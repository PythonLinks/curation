import time
from langdetect import detect

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

    async def previousImportTime(self):
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
        rateLimit = 1
        self.siteRoot = self.getSiteRoot()
        proxy =  self.myAccount()
        pageOfToots = [None]
        count = 0
        rateLimit = 1
        self.importTime = time.time()
        self.contentByTime = self.getSiteRoot().contentByTime

        accountName = context.mastodonId
        user = proxy.account_search(accountName)[0]
        
        while pageOfToots and (count <= rateLimit):
           count += 1 
           pageOfToots = proxy.account_statuses(user.id,
                       max_id=maxId,
                       min_id=None,
                       since_id=None,
                       limit=None)
           if pageOfToots:
              minId  = self.processToots(
                  pageOfToots,allToots)
           else:
             context.crawledToStart = True
        context.backTo = minId
        #self.fetchArticles(self.allToots)
        Form.update(self)


    def processToots(self,pageOfToots,allToots):
        context = self.context
        breakpoint()        
        for toot in pageOfToots:
           if not toot.visibility == 'public':
               continue

           content = toot.content
           hashtags = []
           soup = BeautifulSoup(content, 'html.parser')
           
           text = soup.text
           language = detect(text)
           if language == 'fr':
               continue

           urls  = soup.find_all('a')
           for item in urls:
               if 'mastodon.social'in item['href'].lower():
                   hashtags.append(item.text)
                   item.extract()
           urls = soup.find_all('a')
           if len(urls) != 1:
               continue
           url = urls [0].text
           if url == None:
               continue
           try:
              if self.siteRoot.existsRemoteURL(url):
                  continue
           except:
                 breakpoint()
                 
           if "uncensorednews.us" in url.lower():
                  continue

           importTime = self.previousImportTime()
           tootId = toot.id
           new = TootedArticle(url,content,importTime,tootId)
           new.tags = ' '.join(hashtags)
           new.__parent__ = self.context
           new.__name__ = tootId
           new.articleURL = url
           new.numberOfBoosts = toot.reblogs_count
           new.numberOfFavorites = toot.favourites_count
           #self.context[str(tootId)] = new
           print (url)
           if url in allToots:
               breakpoint()
           allToots[url] = new
          
        minId = pageOfToots[-1].id               
        return minId

    def render(self):
        return "Number of toots = " + str(len(self.allToots))
    
    
