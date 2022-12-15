import time
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.remote.mastodon.basebot import BaseBot
from cromlech.browser.exceptions import HTTPFound
from zopache.remote.mastodon.interfaces import IServer, IMastodonAccount
from zopache.remote.rss import RSSBase
from zopache.remote.mastodon.toot import TootedArticle
from bs4 import BeautifulSoup

import re
regexp = re.compile('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

@form_component
@context(IMastodonAccount)
@target(IView)
@name("crawl")
class CrawlMastodon(Form,BaseBot,RSSBase):

    #First the title
    @property
    def title(self):
        title = "Download the toots for "
        title += self.context.mastodonId
        return  title

    subTitle = "If there are a lot of toots, it can take a while. "

    def previousImportTime(self):
            time = self.importTime + 1
            while True:
                time -= 1
                if - time not in self.contentByTime:
                    self.importTime = time
                    return time
            raise Exception("No Possible times were found!")

    
    def update(self):
        context = self.context
        self.allToots = allToots =  {}
        maxId = None
        rateLimit = 10
        self.siteRoot = self.getSiteRoot()
        proxy =  self.myAccount()
        pageOfToots = [None]
        count = 0
        rateLimit = 10
        breakpoint()
        pageCount = 0
        self.importTime = time.time()
        self.contentByTime = self.getSiteRoot().contentByTime
        accountName = context.mastodonId
        user = proxy.account_search(accountName)[0]
           
        while pageOfToots and (count <= rateLimit):
           pageOfToots = proxy.account_statuses(user.id,
                        max_id=self.context.minId,
                       min_id=None,
                       since_id=None,
                       limit=1000)

           pageCount += 1 
           count += 1

           if pageOfToots:
              self.processToots(
                  pageOfToots,allToots)
           else:
             context.crawledToStart = True
           
        #self.fetchArticles(self.allToots)
        Form.update(self)
        print ("PAGECOUNT = ", pageCount)


    def processToots(self,pageOfToots,allToots):
        context = self.context

        for toot in pageOfToots:
           if not toot.visibility == 'public':
               continue

           if context.minId == None:
               context.minId = toot.id
           elif toot.id < context.minId:
                context.minId = toot.id


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

           self.removeHashTags(soup)

           urls  = soup.find_all('a')

           for item in urls:
               if 'mastodon.social'in item['href'].lower():
                   item.replace_with(item.text)
                   
           soup.smooth()        
           urls = soup.find_all('a')
           if len(urls) != 1:
               continue
           url = urls [0].text
           if not url:
               continue
                 
           if "uncensorednews.us" in url.lower():
                  continue

           if self.siteRoot.existsRemoteURL(url):
                  continue

           urlLength = len(url)
           tootlength = len (toot.text)
           if tootLength - urlLength < 30:
               continue

           importTime = self.previousImportTime()
           tootId = toot.id
           new = TootedArticle(url,content,importTime,tootId)
           new.tags = ' '.join(self.textTags)
           new.__parent__ = self.context
           new.__name__ = tootId
           new.articleURL = url
           new.numberOfBoosts = toot.reblogs_count
           new.numberOfFavorites = toot.favourites_count
           id = 'toot' + str(tootId)
           if not id in self.context:
              self.context[id] = new
           else:
              pass
               
           if not url in allToots:
               allToots[url] = new
          

    def render(self):
        return "Number of toots = " + str(len(self.allToots))

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
                       tag.decompose()
            else:
               for tag in sequence:
                   self.textTags.append(tag.text)                   
                   tag.replace_with(tag.text)
            pass
        
    def isHashTag(self,tag):
       try:
           if tag.name == 'a':
              if tag.text[0] == '#':
                  return True
       except:
           pass
       return False    

