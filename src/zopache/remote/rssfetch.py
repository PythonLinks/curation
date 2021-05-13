import feedparser

from zopache.core.interfaces import ITreeSecurity
from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.remote.rssdownload import getRSS
from zopache.pages.interfaces import IPage
from zopache.remote.rss import IRSSBase
from zopache.crud.getimage import createImageIn
from zopache.core.interfaces import ITreeSecurity


async def processRssResponse(url,response):
          html  =  await response.text()
          feed = feedparser.parse(html)
          entries = feed['entries']
          for article in entries:
               permaLink = article['id']
          return  ('Success', url, entries)

async def processImageResponse(url,response):
          response.content  =  await response.read()          
          return  ('Success' ,url,response)

@form_component
@context(IPage)
@crom.target(IView)
@name("getrss")
@permissions('Manage')
@implementer(ITreeSecurity)
class GetRSS(Form):
    title = "Download the RSS Feeds"
    subTitle = "To get the newest news."
    def update(self):
           urls = []
           feedsByURL = {}
           for item in self.context.allBlogObjects():
               if IRSSBase.providedBy(item):
                   rssURL =  item.rssURL
                   urls.append (rssURL)
                   feedsByURL [rssURL] = item

           result = getRSS(urls)
           for key, value in result.items():
               feed = feedsByURL [key]
               feed.createArticles(value,self)

           self.status='RSS Feeds were downloaded.'
           Form.update(self)

           
@form_component
@context(IPage)
@crom.target(IView)
@name("getImages")
@permissions('Manage')
@implementer(ITreeSecurity)
class GetImages(Form):
    title = "Download the Article Images"
    subTitle = "To get the newest pictures."
    def update(self):
           urls = []
           articlesByURL = {}
           for article in self.context.allBlogObjects():
               if IRSSArticle.providedBy(item):
                 if not 'Logo' in item:
                   if getattr(item,'image',''):        
                       imageURL =  article.image
                       urls.append (imageURL)
                       articlesByURL [imageURL] = item

           result = getRSS(urls, processImageResponse)
           for key, value in result.items():
               if value.status == 200:      
                   article = articlesByURL [key]
                   createImageIn(article,value)               
           self.status='Images were downloaded.'
           Form.update(self)
           
