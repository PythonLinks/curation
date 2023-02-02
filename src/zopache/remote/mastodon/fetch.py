import time

import transaction

from dolmen.forms.base.markers import FAILURE, SUCCESS

from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.remote.mastodon.basebot import BaseBot
from cromlech.browser.exceptions import HTTPFound
from zopache.remote.mastodon.interfaces import IServer, IMastodonAccount
from zopache.remote.rss import RSSBase
from zopache.remote.mastodon.toot import Toot
from zopache.remote.rssdownload import fetchAll
from zopache.remote.news.mastodonarticles import MastodonArticles
from zopache.remote.news.article import Article

import re
regexp = re.compile('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

@form_component
@context(IMastodonAccount)
@target(IView)
@name("reset")
class Reset(Form,BaseBot,RSSBase):
    title = "Reset this mastodon Account"
    subtitle = "So you can crawl it again"
    
    def update(self):
        context = self.context
        context.reset()
        self.status='Account was reset.'
        
@form_component
@context(IMastodonAccount)
@target(IView)
@name("fetch")
class CrawlMastodon(Form,BaseBot,RSSBase):

    #First the title
    @property
    def title(self):
        title = "Download the toots for "
        title += self.context.mastodonId
        return  title


    def previousImportTime(self,time):
            while True:
                time -= 1
                if - time not in self.contentByTime:
                    return time
            raise Exception("No Possible times were found!")
        
    def getAccountName(self,toot):
        accountName = toot.account.acct
        if not '@' in accountName:
            accountName += "@mastodon.social"
        return accountName
    
    def getAccount(self,toot):
        root = self.siteRoot
        feeds = root['mastodon-feeds']
        accountName = self.getAccountName(toot)
        account = feeds.get(accountName,None)
        if account == None:
           account = RemoteAccount()
           account.title = toot.account.username
           feeds [accountName] = account
        return account    
        
    def update(self):
        self.duplicates = 0
        self.startTime = time.time()
        self.siteRoot = self.getSiteRoot()
        proxy =  self.myAccount()
        pageOfToots = [None]
        count = 0
        pageCount = 0
        self.contentByTime = self.getSiteRoot().contentByTime
        importedAccount = self.context
        importedAccountName = importedAccount.mastodonId
        user = proxy.account_search(importedAccountName)[0]

        self.mastodonArticles =self.siteRoot.get('mastodon-articles',None)
        if self.mastodonArticles == None:
            self.mastodonArticles = MastodonArticles()
            self.siteRoot['mastodon-articles'] = self.mastodonArticles
        
        while pageOfToots and (proxy.ratelimit_remaining > 3):

           loopStart = time.time() 
           if self.duplicates > 5:
               print ("EVERYTHING IS DOWNLOADED")
               break
           maxId = importedAccount.minId
           minId = None
           if importedAccount.crawledToStart:
              maxId = None
              
           print (".", end = "")
           self.allToots=allToots = set()
           self.newArticles = newArticles = set()
           self.oldarticles = oldArticles = set()
           pageOfToots = proxy.account_statuses(user.id,
                       max_id=maxId,
                       min_id=minId,
                       since_id=None,
                       limit=1000)


           pageCount += 1 
           count += 1

           if pageOfToots:
              self.processToots(
                  pageOfToots,allToots,newArticles)
           else:
             importedAccount.crawledToStart = True
           self.postProcessPage(allToots,newArticles,oldArticles)
           loopEnd = time.time()
           print ("LoopTime = ", loopEnd - loopStart)
        Form.update(self)
        print ("PAGECOUNT = ", pageCount)

        
    def postProcessPage(self,allToots,newArticles,oldArticles):
           #Until you successfull fetch the article, 
           #and add it to the
           #Parent, it will not be in contentByTime. 
           for item in newArticles:
                  del self.contentByTime[-item.importTime]
           self.fetchArticles (newArticles | oldArticles)
           for toot in allToots:
               url = toot.articleURL
               article = self.siteRoot.existsRemoteURL(url)
               if article:
                  toot.article = article
                  article.addToot(toot)
                  del toot.articleURL   
               
           transaction.manager.commit()
        
    def fetchArticles(self,articles):
        view = self
        result = fetchAll(articles,view, allowedTime = 20)
        for item in result:
            if item[0] ==  FAILURE:  
               view.submissionErrors.append("ERROR: " + str(item[1:]))
               if not 'status' in str(item[1:] ):
                  print ( 'FAILURE' + str(item[1:] ))
        self.status='RSS Feeds were downloaded.'

        
    def processToots(self,pageOfToots,allToots,newArticles):
        root = self.siteRoot
        contentByTime = root.contentByTime

        for toot in pageOfToots:
           account = self.getAccount(toot)
           importedAccount = self.context
           if  toot.visibility in ['private','direct']:
               continue
           tootId = str(toot.id)
           if oldToot :=  account.get(tootId,None):
               self.duplicates += 1
               oldToot.updateValue(
                                'numberOfBoosts',
                                toot.reblogs_count)
               oldToot.updateValue(
                                'numberOfFavorites',
                                toot.favourites_count)
               continue
           
           if importedAccount.minId == None:
               importedAccount.minId = tootId
               
           elif tootId < importedAccount.minId:
                importedAccount.minId = tootId
                
           account = self.getAccount(toot)
           new, articleURLs = Toot().createToot(toot,account)
           if new != None:
               if new.name == None:
                  print ("Error: new.name == None")
                  break
               try:
                  account[new.name] = new
               except:
                   print ("ERROR: account[new.name] = new")
                   break
               allToots.add( new)               
               
           #CALCULATE THE LINK IMPORT TIME
           try:
               importTime = self.getPublicationTime(toot)
           except:
               importTime = time.time()
           importTime = int(importTime)

           for url in articleURLs:           
               #FIRST GET THE ARTICLE
               #If the article exists, publicationApprove it
               #And possibly add a Logo.                     
               article = self.siteRoot.existsRemoteURL(url)
               if article == None:
                   anArticle = Article()
                   anArticle.articleURL = url
                   anArticle.parent = self.mastodonArticles
                   importTime = self.previousImportTime(importTime)
                   anArticle.importTime = importTime
                   newArticles.add(anArticle)
                   self.contentByTime[-importTime] = anArticle
               else:
                   #if publicationApproved, it will have a logo 
                   if not article.publicationApproved:
                       oldArticles.add (article)
                       article.publicationApproved = True
            
    def getPublicationTime(self,toot):           
        publicationTime = time.mktime(toot.created_at.timetuple())
        return int (publicationTime)

    def render(self):
        print ("Duration = ", str((time.time() - self.startTime)/60))
        return (
            "Duration =  " + str((self.startTime - time.time())/60) +
            "<br> New toots = " + str(len(self.allToots)) + 
            "<Br> Total Toots " + str(len(self.context)) )
                

               
    """
    def debug(self,pageOfToots):
        from bs4 import BeautifulSoup
        for item in pageOfToots:
       yes
    if not item.reblog:
                soup = BeautifulSoup(item.content, 'html.parser')
                print()
                print( item.created_at.ctime())
                print (soup.get_text())

                
    """
    """
    def fixTime(self,toot):
            root = self.siteRoot
            account = self.context
            contentByTime = self.contentByTime        
            if tootedArticle := account.localArticles.get(toot.id,None):
               publicationTime = None 
               try:
                   publicationTime = self.getPublicationTime(toot)
               except:
                   pass
               if publicationTime:
                  root.unIndexItem(tootedArticle)
                  importTime = self.previousImportTime(publicationTime)
                  tootedArticle.importTime = importTime
                  root.indexItem(tootedArticle) 
    """
