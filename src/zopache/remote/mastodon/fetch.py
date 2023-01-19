import time
from bs4 import BeautifulSoup

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
from zopache.remote.mastodon.toot import TootedArticle
from zopache.remote.rssdownload import fetchAll


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
        print ("Acount Name")
        user = proxy.account_search(accountName)[0]
        print ("Acount Name DONE ")               
               
        

        while pageOfToots and (proxy.ratelimit_remaining > 3):

           loopStart = time.time() 
           if self.duplicates > 10:
               print ("EVERYTHING IS DOWNLOADED")
               #break
           maxId = account.minId
           minId = None
           if account.crawledToStart:
              maxId = None
              
           print (".", end = "")
           self.allToots=allToots =  {}
           
           pageOfToots = proxy.account_statuses(user.id,
                       max_id=maxId,
                       min_id=minId,
                       since_id=None,
                       limit=1000)

           pageCount += 1 
           count += 1

           if pageOfToots:
              self.processToots(
                  pageOfToots,allToots)
           else:
             account.crawledToStart = True
           self.postProcessPage(allToots)
           loopEnd = time.time()
           print ("LoopTime = ", loopEnd - loopStart)
        Form.update(self)
        print ("PAGECOUNT = ", pageCount)

        
    def postProcessPage(self,allToots):
           #Until you fetch the article, give it a name,
           #and add it to the
           #Parent, it will not be in contentByTime. 
           for item in allToots.values():
                  del self.contentByTime[- item.importTime]
           self.fetchArticles (allToots.values())
           transaction.manager.commit()

        
    def fetchArticles(self,articles):
        view = self
        result = fetchAll(articles,view, allowedTime = 30)
        for item in result:
            print (result[0])
            if item[0] ==  FAILURE:  
               view.submissionErrors.append( "ERROR:" + str(item [1]))
               print ("item 1", str(item [1]))               
        self.status='RSS Feeds were downloaded.'

    def processToots(self,pageOfToots,allToots):
        account = self.context
        root = self.siteRoot
        contentByTime = self.contentByTime
        for toot in pageOfToots:
           tootId = toot.id           
           if oldToot :=  account.localArticles.get(tootId,None):
               self.duplicates += 1
               oldToot.numberOfBoosts = toot.reblogs_count
               oldToot.numberOfFavorites = toot.favourites_count
           
           if not toot.visibility == 'public':
               continue

           if account.minId == None:
               account.minId = tootId
               
           elif tootId < account.minId:
                account.minId = tootId

           content = toot.content
           self.hashTags = []
           self.textTags = []           
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

           soup = self.removeHashTags(soup)
           urls  = soup.find_all('a')

           for item in urls:
               if 'mastodon.social'in item['href'].lower():
                   item.replace_with(item.text)
                   
           urls = soup.find_all('a')
           if len(urls) != 1:
               continue
           url = urls [0].text
           urls[0].replace_with('')
           soup.smooth()        
           if not url:
               continue
                 
           if "uncensorednews.us" in url.lower():
                  continue

           urlLength = len(url)
           tootLength = len (toot.content)
           if tootLength - urlLength < 30:
               continue
           
           if url in allToots:
              continue

           #ALL TESTS HAVE PASSED, YOU CAN DELETE THE OLD RSS ARTICLE
           #AND REPLACE IT
           rssParent = None
           if rssArticle := self.siteRoot.existsRemoteURL(url):
              rssParent = rssArticle.parent 
              if self.className(rssArticle) == "RSSArticle":
                  
                 if rssArticle.publicationApproved:
                     continue
                 rssArticle.preDeleteProcess(self)
                 del rssArticle.parent[rssArticle.name]
              else:
                 continue 
           tootURL = toot.url
           soup = self.removeEmptyParagraphs(soup)
           content = str(soup)
           try:
               importTime = self.getPublicationTime(toot)
           except:
               importTime = time.time()
               
           importTime = int(importTime)
           importTime = self.previousImportTime(importTime) 
           new = TootedArticle(url,content,importTime,tootId,tootURL)
           new.tags = ' '.join(self.textTags)
           new.__parent__ = rssParent or account
           new.curator = account
           new.articleURL = url
           new.hasMedia =  True if toot.media_attachments else False
           new.userId = toot.account.acct
           new.numberOfBoosts = toot.reblogs_count
           new.numberOfFavorites = toot.favourites_count

           if not url in allToots:
               allToots[url] = new               
               self.contentByTime[-importTime] = new
               
    def getPublicationTime(self,toot):           
        publicationTime = time.mktime(toot.created_at.timetuple())
        return int (publicationTime)

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
        self.hashTags = hashTags =  []
        
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
                       self.textTags.append(tag.text)
                       tag.replace_with('')
            else:
               for tag in sequence:
                   self.textTags.append(tag.text)                   
                   tag.replace_with(tag.text)
        return soup
        
    def isHashTag(self,tag):
       try:
           if tag.name == 'a':
              if tag.text[0] == '#':
                  return True
       except:
           pass
       return False    

