
import re
import time
from urllib.parse import urlparse

import transaction

from dolmen.forms.base.markers import FAILURE, SUCCESS

from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.remote.mastodon.basebot import BaseBot
from cromlech.browser.exceptions import HTTPFound
from zopache.remote.mastodon.interfaces import IServer, IRemoteAccount
from zopache.remote.rss import RSSBase
from zopache.remote.mastodon.toot import Toot
from zopache.remote.rssdownload import fetchAll
from zopache.remote.news.mastodonarticles import MastodonArticles
from zopache.remote.news.article import Article
from zopache.remote.mastodon.remoteaccount import RemoteAccount
from zopache.core.transactionnote import TransactionNote
from zopache.core.baseform import Form


regexp = re.compile('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')


crawlBackSeconds = 3600 * 24 * 5 #5 Days

@view_component
@context(IRemoteAccount)
@target(IView)
@name("reset")
@permissions('Manage')
class Reset(Form):
    title = "Reset this mastodon Account"
    subtitle = "So you can crawl it again"

    
    def update(self):
        context = self.context
        context.reset()
        self.status='Account was reset.'
        
@view_component
@context(IRemoteAccount)
@target(IView)
@name("fetchxyz")
#@permissions('Manage')
class CrawlMastodon(Form,BaseBot,RSSBase,TransactionNote):

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
            accountName =  accountName + "@mastodon.social"
        if not accountName.startswith("@"):
            accountName = "@" + accountName
        return accountName
    
    def getAccount(self,toot):
        root = self.siteRoot
        feeds = root['mastodon-accounts']
        accountName = self.getAccountName(toot)
        account = feeds.get(accountName,None)
        if account == None:
           account = RemoteAccount()
           account.title = toot.account.username
           account.mastodonId = accountName
           feeds [accountName] = account
        return account    
        
    def update(self):
        self.duplicates = 0
        self.startTime = time.time()
        self.siteRoot = self.getSiteRoot()
        proxy =  self.myAccount()
        pageOfToots = [None]
        pageCount = 0
        self.contentByTime = self.getSiteRoot().contentByTime
        account = self.context
        accountName = account.mastodonId
        user = proxy.account_search(accountName)[0]

        self.mastodonArticles =self.siteRoot.get('mastodon-articles',None)
        if self.mastodonArticles == None:
            self.mastodonArticles = MastodonArticles()
            self.siteRoot['mastodon-articles'] = self.mastodonArticles

        startTime = time.time()
        pageOfToots = [None]
        
        if account.crawledToStart == True:
            maxId = None
            age = 0
            while (pageOfToots and
                (proxy.ratelimit_remaining > 3) and
                (age < 6)):
                pageOfToots = proxy.account_statuses(user.id,
                       max_id=maxId,
                       limit=1000)
                if len (pageOfToots) > 0:
                    maxId = pageOfToots [-1].id
                age = self.processPage(pageOfToots,account)
                pageCount += 1

        else:    #First Import
            while pageOfToots and (proxy.ratelimit_remaining > 3):
                maxId = account.maxId
                pageOfToots = proxy.account_statuses(user.id,
                       max_id=maxId,
                       limit=1000)
                if len (pageOfToots) > 0:
                    account.setMaxId(pageOfToots[-1].id)
                self.processPage(pageOfToots,account)
                pageCount += 1                         

        Form.update(self)
        print ("PAGECOUNT = ", pageCount)
        self.getSiteRoot().lastMastodonFetchTime = startTime
        print ("Crawled To Start", account.crawledToStart)
        account.modificationTime = startTime
             
    def processPage(self,pageOfToots,account):
           loopStart = time.time()        
           self.allToots=allToots = set()
           self.newArticles = newArticles = {}
           self.oldArticles = oldArticles = set()

           if pageOfToots:
               self.processToots(
                   pageOfToots,allToots,newArticles)
               self.postProcessPage(allToots,newArticles,oldArticles)
               loopEnd = time.time()
               loopTime = int(loopEnd - loopStart)
               lastToot = pageOfToots [-1]
               age = loopStart - self.getPublicationTime(lastToot)
               age = age/(3600 *24)
               age = int(age)
               print ("AGE = ", age, end = "")
               print ("\nLoopTime = ", loopTime)
           else:
               age = 0
               print ("CRAWLED TO START")
               account.crawledToStart = True
           return age

           
    def postProcessPage(self,allToots,newArticles,oldArticles):
           #Until you successfull fetch the article, 
           #and add it to the
           #Parent, it will not be in contentByTime. 
           for item in newArticles.values():
                  del self.contentByTime[-item.importTime]
           allArticles = set(newArticles.values()) | oldArticles
           self.fetchArticles (allArticles)
           for toot in allToots:
               for url in toot.articleURLs:
                   article = self.siteRoot.existsRemoteURL(url)
                   if article != False:
                      toot.addArticle(article) 
                      article.addToot(toot)
                      
           #Since the created articles did not know about
           #the relevant toots.
           root = self.siteRoot
           for article in newArticles.values():
               if article.name:
                   root.unIndexItem(article)
                   root.indexItem(article)
           self.describeTransactionWithText(
                "Fetching from: " + self.context.mastodonId
           )                   
           transaction.manager.commit()
        
    def fetchArticles(self,articles):
        view = self
        result = fetchAll(articles,view, allowedTime = 20)
        for item in result:
            if item[0] ==  FAILURE:  
               view.submissionErrors.append("ERROR: " + str(item[1:]))
               if not 'status' in str(item[1:] ):
                  if not "TIME OUT" in str(item): 
                     try:
                         print ("\n", str(item))
                     except:
                         print ("\n", type(item))
                         
        self.status='RSS Feeds were downloaded.'

        
    def processToots(self,pageOfToots,allToots,newArticles):
        root = self.siteRoot
        contentByTime = root.contentByTime
        for toot in pageOfToots:

           account = self.context
           tootId = str(toot.id)
                
           message, new  = Toot().createToot(toot,account)
           #if new != None:
           #  if not new.asText.startswith('@'):
           #    print (new.asText[0:200])
           #    print (message)
           #    break point()
           if message != "SUCCESS":
               continue
           allToots.add(new)           
           for url in new.articleURLs:
               article = self.siteRoot.existsRemoteURL(url)
               if article == False:
                 if url not in newArticles:
                     anArticle = Article(toot,
                                       url,
                                       account,
                                       self.mastodonArticles,
                                       root)
                     importTime = self.getPublicationTime(toot)
                     importTime = int(importTime)
                     importTime = self.previousImportTime(importTime)
                     anArticle.importTime = importTime

                     newArticles[url] = anArticle
                     self.contentByTime[-importTime] = anArticle
                     print (".", end = "") 
               else:                    
                   if not article.publicationApproved:
                       article.publicationApproved = True
                       self.oldArticles.add (article)

                       
    
    def getPublicationTime(self,toot):           
        try:
            publicationTime = time.mktime(toot.created_at.timetuple())
        except:    
            publicattinTime = time.time()
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
