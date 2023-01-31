import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

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

hostNamesToIgnore = {"uncensorednews.us",
                     "takvera.blogspot.com"}

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

    subTitle = "If there are a lot of toots, it can take a while. "

    def previousImportTime(self,time):
            while True:
                time -= 1
                if - time not in self.contentByTime:
                    return time
            raise Exception("No Possible times were found!")

    def update(self):
        self.duplicates = 0
        account = self.context
        self.startTime = time.time()
        self.siteRoot = self.getSiteRoot()
        proxy =  self.myAccount()
        pageOfToots = [None]
        count = 0
        pageCount = 0
        self.contentByTime = self.getSiteRoot().contentByTime
        accountName = account.mastodonId
        user = proxy.account_search(accountName)[0]

        self.mastodonArticles =self.siteRoot.get('mastodon-articles',None)
        if self.mastodonArticles == None:
            self.mastodonArticles = MastodonArticles()
            self.siteRoot['mastodon-articles'] = self.mastodonArticles
        
        while pageOfToots and (proxy.ratelimit_remaining > 3):

           loopStart = time.time() 
           if self.duplicates > 5:
               print ("EVERYTHING IS DOWNLOADED")
               break
           maxId = account.minId
           minId = None
           if account.crawledToStart:
              maxId = None
              
           print (".", end = "")
           self.allToots=allToots = set()
           self.newArticles = newArticles = set()
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
             account.crawledToStart = True
           self.postProcessPage(allToots,newArticles)
           loopEnd = time.time()
           print ("LoopTime = ", loopEnd - loopStart)
        Form.update(self)
        print ("PAGECOUNT = ", pageCount)

        
    def postProcessPage(self,allToots,newArticles):
           #Until you successfull fetch the article, 
           #and add it to the
           #Parent, it will not be in contentByTime. 
           for item in newArticles:
                  del self.contentByTime[-item.importTime]
           self.fetchArticles (newArticles)
           for toot in allToots:
               url = toot.articleURL
               if article := self.siteRoot.existsRemoteURL(url):
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

    def updateValue(self,item,name,newValue):
        if getattr(item,name,None) != newValue:
            setattr(item,name,newValue)
        
    def processToots(self,pageOfToots,allToots,newArticles):
        account = self.context
        root = self.siteRoot
        contentByTime = root.contentByTime
        for toot in pageOfToots:
           if  toot.visibility in ['private','direct']:
               continue
           tootId = str(toot.id)
           if oldToot :=  account.get(tootId,None):
               self.duplicates += 1
               self.updateValue(oldToot,
                                'numberOfBoosts',
                                toot.reblogs_count)
               self.updateValue(oldToot,
                                'numberOfFavorites',
                                toot.favourites_count)
               continue
           
           if account.minId == None:
               account.minId = tootId
               
           elif tootId < account.minId:
                account.minId = tootId

           content = toot.content
           soup = BeautifulSoup(content, 'html.parser')
           text = soup.text
           if not soup.text.strip():
               continue
           
           try:
                language = detect(text)
           except LangDetectException as e:
               continue
           if language != 'en':
               continue

           soup, textTags = self.removeHashTags(soup)
           urls  = soup.find_all('a')
           if len(urls) != 1:
               continue
           url = urls [0]["href"]
           if not url:
               continue
           hostName = urlparse(url).hostname
           if not hostName:
               continue
           if hostName.lower() in hostNamesToIgnore:
                  continue
           urls[0].replace_with('')
           soup.smooth()        

           #CALCULATE THE LINK IMPORT TIME
           try:
               importTime = self.getPublicationTime(toot)
           except:
               importTime = time.time()
           importTime = int(importTime)
           importTime = self.previousImportTime(importTime)

           #FIRST GET THE ARTICLE
           #If the article exists, publicationApprove it
           #And possibly add a Logo.                     
           article = self.siteRoot.existsRemoteURL(url)
           if article == None:
              anArticle = Article()
              anArticle.articleURL = url
              anArticle.parent = self.mastodonArticles
              anArticle.importTime = importTime
              newArticles.add(anArticle)
              self.contentByTime[-importTime] = anArticle
           else:
              #if publicationApproved, it will have a logo 
              if not article.publicationApproved:
                 newArticles.add (article)
                 article.publicationApproved = True
            
           #NOW CREATE THE TOOT   
           tootURL = toot.url
           soup = self.removeEmptyParagraphs(soup)
           content = str(soup)
           new = Toot(url,content,tootId,tootURL)
           new.tags = ' '.join(textTags)
           new.parent =  account
           name = str(tootId)                     
           new.hasMedia =  True if toot.media_attachments else False
           new.userId = toot.account.acct
           new.numberOfBoosts = toot.reblogs_count
           new.numberOfFavorites = toot.favourites_count
           account [name] = new                     
           allToots.add( new)               
               
    def getPublicationTime(self,toot):           
        publicationTime = time.mktime(toot.created_at.timetuple())
        return int (publicationTime)

    def render(self):
        print ("Duration = ", str((time.time() - self.startTime)/60))
        return (
            "Duration =  " + str((self.startTime - time.time())/60) +
            "<br> New toots = " + str(len(self.allToots)) + 
            "<Br> Total Toots " + str(len(self.context)) )
                

    def removeEmptyParagraphs(self,soup):
        for item in soup:
            if not item.text.strip():
               item.replace_with('')
        return soup       

               
    #Iterate through destroying all but the last hash tag. 
    def removeHashTags(self,soup):
        hashTags =  []
        textTags = []                        
        
        previousTag = None
        lastWasHashTag = False
        contents = soup.contents
        for paragraph in contents:
            for tag in paragraph:
                #skip spaces
                if not tag.text.strip():
                    continue
                if self.isHashTag(tag):
                    if not lastWasHashTag:
                        hashTags.append([])
                    hashTags [-1].append(tag)
                    lastWasHashTag = True
                else:
                    lastWasHashTag = False 

        for sequence in hashTags:

            if len (sequence) > 1:
               for tag in sequence:
                       textTags.append(tag.text)
                       tag.replace_with('')
            else:
               for tag in sequence:
                   textTags.append(tag.text)                   
                   tag.replace_with(tag.text)
        return soup,textTags
        
    def isHashTag(self,tag):
       try:
           if tag.name == 'a':
              if tag.text[0] == '#':
                  return True
       except:
           pass
       return False    

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
