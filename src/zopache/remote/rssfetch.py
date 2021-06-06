import feedparser

from zopache.remote.rss import IRSSBase, IRSS
from zopache.core.interfaces import ITreeSecurity
from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.remote.rssdownload import fetchAll
from zopache.pages.interfaces import IPage
<<<<<<< HEAD
from zopache.crud.getimage import createImageIn
from zopache.core.interfaces import ITreeSecurity
from zopache.remote.irss import IRSSBase
=======
from zopache.remote.rss import IRSSBase
from zopache.crud.getimage import createImageInFrom
from zopache.core.interfaces import ITreeSecurity
>>>>>>> ef56173d3c1a0bc32a067cfed31152cb85de0cb7
from zopache.remote.rssarticle import IRSSArticle, RSSArticle

def callTwice(self):
        articles = []
        for  item  in self.context.allBlogObjects():
               if IRSSArticle.providedBy(item):
                   if not 'Logo' in item:
                      articles.append(item)
        results = fetchAll(articles, self)
        for item in results:
            if item == None:
               continue
            (article, content, contentType) = item
            #print ("CREATING IMAGE" + article.name)
            createImageInFrom(article,content,contentType)



def getImages(urls):
          return getRSS(urls,processImageResponse)

def getArticles(urls):
          return getRSS(urls, processRssResponse)

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
        feeds = []
        for  item  in self.context.allBlogObjects():
               if IRSS.providedBy(item):
                      feeds.append(item)
        fetchAll(feeds,self)
        callTwice(self)
        callTwice(self)
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
<<<<<<< HEAD
           urls = []
           articlesByURL = {}
           for article in self.context.allBlogObjects():
               if IRSSArticle.providedBy(article):
                  imageURL = article.getImageURL()
                  if imageURL:
                       urls.append (imageURL)
                       articlesByURL [imageURL] = article        
           result = getRSS(urls, processImageResponse)
           for key, value in result.items():
               if value.status == 200:      
                   article = articlesByURL [key]
                   createImageIn(article,value)               
           self.status='Images were downloaded.'
           Form.update(self)
=======
        callTwice(self)
        callTwice(self)
        self.status='Images were downloaded.'
        Form.update(self)
>>>>>>> ef56173d3c1a0bc32a067cfed31152cb85de0cb7
           
