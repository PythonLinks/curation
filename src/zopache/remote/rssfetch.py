import feedparser

from zopache.remote.irss import IRSSBase, IRSS
from zopache.core.interfaces import ITreeSecurity
from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.remote.rssdownload import fetchAll
from zopache.pages.interfaces import ISiteRootPage, IPage
from zopache.crud.getimage import createImageInFrom
from zopache.core.interfaces import ITreeSecurity
from zopache.remote.rssarticle import IRSSArticle, RSSArticle
from itertools import islice

def callTwice(view):
      allArticles = view.getSiteRoot().newestArticles.values()
      return callTwiceCore(view,allArticles)
   
def callTwiceCore(view,allArticles):
   someArticles = []
   articles = []
   for item in islice(allArticles,0,100 ):
       if item.__class__.__name__ == 'RSSArticle':
          someArticles.append(item)          
   for i in range(5):
      articles = someArticles [0:20]
      someArticles = someArticles[20: ]
      results = fetchAll(articles, view)
      for item in results:
            if len(item) == 2:
               print (item[0], item  [1])
               continue
            (article, content, contentType) = item
            print ("CREATING IMAGE " + article.name)
            createImageInFrom(article,content,contentType)



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
                  if item.rssApproved:   
                      feeds.append(item)
        result = fetchAll(feeds,self)
        for item in result:
            if item != None:  
              if len(item) == 2:
                  print ("ERROR", item[0], item[1])
        callTwice(self)
        callTwice(self)
        self.status='RSS Feeds were downloaded.'
        Form.update(self)

 
from cromlech.browser.interfaces import IPublicationRoot
          
@form_component
@context(ISiteRootPage)
@crom.target(IView)
@name("getImages")
@permissions('Manage')
@implementer(ITreeSecurity)
class SiteRootGetImages(Form):
    title = "Download the Article Images"
    subTitle = "To get the newest pictures."
            
    def update(self):
        callTwice(self)
        callTwice(self)
        self.status='Images were downloaded.'
        Form.update(self)


@form_component
@context(IRSS)
@crom.target(IView)
@name("getImages")
@permissions('Manage')
@implementer(ITreeSecurity)
class GetImages(Form):
    title = "Download the Article Images"
    subTitle = "To get the newest pictures."
            
    def update(self):
        articles = list(self.context.values())
        callTwiceCore(self,articles)
        callTwiceCore(self,articles)
        self.status='Images were downloaded.'
        Form.update(self)
        
