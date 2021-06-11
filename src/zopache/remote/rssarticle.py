import time
from zope.interface import Interface
from zope import schema
from zopache.pages.interfaces import IPage
from zopache.pages.page import Page
from zopache.core.viewdecorators import *
from zopache.crud.getimage import createImageInFrom
from webpreview import web_preview
from zopache.remote.rssdownload import fetch
from zopache.remote.irss import IRSSArticle
    
from zopache.remote.voteable import Voteable
from zopache.pages.page import Page    
@implementer (IRSSArticle)
class RSSArticle(Page,Voteable):
    _category = ""
    importTime = 0
    imageURL = ""
    webClass = "RSSLink"
    emailApproved = True
    publicationApproved = False

    def __init__(self):
        importTime=time.time()
        importTime = int(importTime)
        self.importTime = importTime
        Page.__init__(self)
        
    def preDeleteProcess(self,view):
        #Page.preDeleteProcess(self,view)
        localArticles = self.rssFeed.localArticles
        if hasattr(self,'permalink'):
            if self.permalink in localArticles:
                 del localArticles [self.permaLink]
    
    def getCategory(self):
      return self._category

    def moveTo(self,category):
              name = self.__name__
              del self.__parent__[name]
              category [name] = self
              self.__name__ = name
  
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

    def getImportTime(self,siteRoot):
        importTime = self.importTime
        importTime = siteRoot.getImportTime(importTime)
        self.importTime = importTime                                    
        return importTime

    def postAddProcess (self, view = None):
        Page.postAddProcess(self,view = view)
        if "exclusive for subscribers" in self.title.lower():
           self.webApproved = False

        #categories = parentsWhichImplement(self,IRSSCategory)
        #for item in categories:
        #     item.articlesByTime[-self.importTime] = self

        
    def addImage(self):
           if  'Logo' in self:
               return
           imageURL = self.getImageURL()
           if imageURL:
               getImage(self,imageURL)           

    def getImageURL(self):
        if hasattr(self,'imageURL'):
            if self.imageURL != "":
                return self.imageURL           
        elif  hasattr(self,'links'):
            for item in self.links:
                if "image" in item.type:
                    return self.item.href
        return ""

    async def processResponse(self,session, response,view):
        if self.getImageURL():
           content = await response.read()
           return self, content, response.headers['Content-Type']
        else:
            html  =  await response.text()
            result = web_preview(self.articleURL, content = html, parser="html.parser")
            imageURL = result [2]
            if imageURL:
               self.imageURL = imageURL
               response =  await fetch(session, self, view)
               (article, content, contentType) = response               
               return self, content, contentType
            else:
               return self, "NO IMAge urL in page html"





