import time
from bs4 import BeautifulSoup

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

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
@name("fetch")
class CrawlMastodon(Form,BaseBot,RSSBase):

    #First the title
    @property
    def title(self):
        title = "Download the toots for "
        title += self.context.mastodonId
        return  title

    subTitle = "If there are a lot of toots, it can take a while. "

    def previousImportTime(self):
            time = self.importTime 
            while True:
                time -= 1
                if - time not in self.contentByTime:
                    self.importTime = time
                    return time
            raise Exception("No Possible times were found!")

    
    def update(self):
        context = self.context
        self.allToots=allToots =  {}
        self.startTime = time.time()
        self.siteRoot = self.getSiteRoot()
        proxy =  self.myAccount()
        pageOfToots = [None]
        count = 0
        pageCount = 0
        self.importTime = int(time.time()) + 1
        self.contentByTime = self.getSiteRoot().contentByTime
        accountName = context.mastodonId
        user = proxy.account_search(accountName)[0]
        
        rateLimit = 30
        if rateLimit >  proxy.ratelimit_remaining:
            rateLimit  = proxy.ratelimit_remaining - 1
        while pageOfToots and (count <= rateLimit):
           print (".", end = "")
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
        print ("Number of Toots",len(self.context))
        
        #SOMETHING IS FISHY HERE>
        #I SHOULD NOT NEED TO TEST IF IT IS THERE OR NOT. 
        for item in allToots.values():
                del self.contentByTime[- item.importTime]
            
        self.fetchArticles (allToots.values())   
        Form.update(self)
        print ("PAGECOUNT = ", pageCount)
        
    def fetchArticles(self,articles):
        view = self
        result = fetchAll(articles,view)
        for item in result:
            if item[0] ==  FAILURE:  
               view.submissionErrors.append( "ERROR:" + str(item [1:]))
        self.status='RSS Feeds were downloaded.'

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

           if self.siteRoot.existsRemoteURL(url):
                  continue

           urlLength = len(url)
           tootLength = len (toot.content)
           if tootLength - urlLength < 30:
               continue

           tootId = toot.id
           tootURL = toot.url
           soup = self.removeEmptyParagraphs(soup)
           content = str(soup)
           importTime = self.previousImportTime()
           new = TootedArticle(url,content,importTime,tootId,tootURL)
           new.publishedAt = time.mktime(toot.created_at.timetuple())
           new.tags = ' '.join(self.textTags)
           new.__parent__ = self.context
           new.curator = self.context
           new.articleURL = url

           new.numberOfBoosts = toot.reblogs_count
           new.numberOfFavorites = toot.favourites_count

           if not url in allToots:
               allToots[url] = new               
               self.contentByTime[-importTime] = new
               print ("adding ", importTime, tootId )       

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

