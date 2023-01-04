import time
from slugify import slugify

from zope.interface import Interface
from zope import schema
from zope.interface import implementer
from dolmen.container import OrderedBTreeContainer

from zopache.pages.interfaces import IPage, ICategory
from zopache.pages.page import Page
from zopache.core.viewdecorators import *
from zopache.crud.getimage import createImageInFrom
from webpreview import web_preview
from zopache.remote.rssdownload import fetch
from zopache.remote.irss import IRSSArticle
from zopache.core.relatives import parentsWhichImplement
from zopache.crud.getimage import getImage

from zopache.remote.voteable import Voteable
from zopache.pages.page import Page    
    
class BaseArticle(Page):    
    _category = ""
    importTime = 0
    isArticle = True
    imageURL = ""
    description = ""
    emailApproved = True
    publicationApproved = False
    bestApproved = False
    tags = {}
    delay = 0
    def __init__(self):
         #Simpler to not call page initialization.
         #HOPE I DO NOT MISS ANYTHING
         OrderedBTreeContainer.__init__(self)
         self.modificationTime= time.time()
         self.importTime = int(self.modificationTime)


    
    def defaultToot(self,view):        
            twitterId = self.rssFeed.twitterId
            return   (
                self.title +
                "\n\n" +
                self.description +
                "\n\n" +
                self.articleURL +
                (("\n\nBy @" + twitterId.strip() + "@twitter.com")
                    if twitterId else '') +
               "\n\n" +
               "Read more at:  https://UncensoredNews.US/" + self.parent.name + 
               "\n\n" +
                self.tagsAsString() + ' ' +
                self.parentalTags()                 
                )

        
    def tagsAsString(self):
               return" ".join (self.tagsAsArray())

    def tagsAsHTML(self):
               return"<br>".join (self.tagsAsArray())
           
    def tagsAsArray(self):       
               terms = set()
               for tag in self.tags:
                   term = tag["term"]
                   term = "#" + slugify(term)
                   if term not in {"#news","#featured"}:
                       terms.add (term)
               return terms 
           

            
    def getCategory(self):
      return self._category

    def moveTo(self,category):
              name = self.__name__
              del self.__parent__[name]
              category [name] = self
              self.__name__ = name
  
    def setImportTime(self,importTime,root):
        importTime = int(importTime)
        while (True):
           if not root.hasAnythingAt(importTime):
                break;
                importTime += 1
        self.importTime = importTime
            

    def setCategory(self,value):       
        self._category = value
       
    def getSrcSet(self):
        pass
    
    def getDefaultThumbNailURL(self):
        pass

    def getCreationTime(self):
        return self.publishedAt

    def setCreationTime (self, aTime):
        self.__dict__['creationTime'] = aTime
        
    creationTime = property(getCreationTime,setCreationTime)

    #AND NOW RESET  A UNIQUE CREATION TIMES FOR ALL RSS ARTICLES

    def addImage(self):
           if  'Logo' in self:
               return
           imageURL = self.getImageURL()
           if imageURL:
               getImage(self,imageURL)           


@implementer (IRSSArticle)
class RSSArticle(BaseArticle):
    webClass = "RSSLink"

    def getImageURL(self):
        if url:= getattr(self,'imageURL',None):
            return url          
        elif  hasattr(self,'links'):
            for item in self.links:
                if "image" in item.type:
                    return item.href
        return None

    
    def creationDateForHumans(self):
         return time.strftime("%Y-%m-%d",time.localtime(self.publishedAt))
         
    def getAuthor(self,view ):
        author = self.rssFeed
        authorName = author.title
        authorURL = author.remoteURL
        if 'Logo' in author:
            imageURL = view.secureShortURL(context = author) + "/Logo"
        else:    
            topic = self.parent
            imageURL = view.secureShortURL(context = self) + "/Logo"
        return authorName, authorURL, imageURL

    def preDeleteProcess(self,view):
        #Page.preDeleteProcess(self,view)
        localArticles = self.rssFeed.localArticles
        if hasattr(self,'permalink'):
            if self.permalink in localArticles:
                 del localArticles [self.permaLink]
            else:
                raise Exception("That article was not listed in localArticles.")


    def postAddProcess (self, view = None,article = None):
        if "exclusive for subscribers" in self.title.lower():
           self.webApproved = False
        
