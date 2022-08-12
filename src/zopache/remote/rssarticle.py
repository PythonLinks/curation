import time
from slugify import slugify

from zope.interface import Interface
from zope import schema
from dolmen.container import OrderedBTreeContainer

from zopache.pages.interfaces import IPage, ICategory
from zopache.pages.page import Page
from zopache.core.viewdecorators import *
from zopache.crud.getimage import createImageInFrom
from webpreview import web_preview
from zopache.remote.rssdownload import fetch
from zopache.remote.irss import IRSSArticle
from zopache.core.relatives import parentsWhichImplement

from zopache.remote.voteable import Voteable
from zopache.pages.page import Page    
@implementer (IRSSArticle)
class RSSArticle(Page):
    _category = ""
    importTime = 0
    isArticle = True
    imageURL = ""
    webClass = "RSSLink"
    description = ""
    emailApproved = True
    publicationApproved = False
    bestApproved = False
    tags = {}
    _toot = ""    
    def __init__(self):
         #Simpler to not call page initialization.
         #HOPE I DO NOT MISS ANYTHING
         OrderedBTreeContainer.__init__(self)
         self.modificationTime= time.time()
         self.importTime = int(self.modificationTime)

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
        
    def creationDateForHumans(self):
         return time.strftime("%Y-%m-%d",time.localtime(self.publishedAt))
     
    def defaultToot(self):        
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
               "Via https://UncensoredNews.US/" + self.parent.name + 
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
           
    def preDeleteProcess(self,view):
        #Page.preDeleteProcess(self,view)
        localArticles = self.rssFeed.localArticles
        if hasattr(self,'permalink'):
            if self.permalink in localArticles:
                 del localArticles [self.permaLink]
            else:
                raise Exception("That article was not listed in localArticles.")

            
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

    def postAddProcess (self, view = None):
        if "exclusive for subscribers" in self.title.lower():
           self.webApproved = False
        
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
            
            if "This post is for paying subscribers." in html:
               self.webApproved = False
               
            if imageURL:
               self.imageURL = imageURL
               response =  await fetch(session, self, view)
               (article, content, contentType) = response               
               return self, content, contentType
            else:
               return self, "NO IMAge urL in page html"





