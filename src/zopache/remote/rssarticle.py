import time
from zope.interface import Interface
from zope import schema
from zopache.pages.interfaces import IPage
from zopache.pages.page import Page
from zopache.core.viewdecorators import *
from zopache.remote.interfaces import IVoteable
from zopache.crud.getimage import getImage

class IRSSArticle(IPage,IVoteable):

    title = schema.TextLine(
        title = 'Remote Article Name',
        description = 'What is the title of this link?',
        required = True,
    )
    
    articleURL= schema.URI(
        title = 'Article URL',
        description = 'The url of the remote article',
        required = False,
    )
    
    description= schema.Text(
        title = u'Description',
        description = """A brief introduction of this page.  
                        This is used by the search functions.""",
        required = False,
        default = u'',
    )

    source= schema.Text(
        title = 'Content',
        description = 'This is the main content for this page',
        required = False,
        default = '',
    )

    
from zopache.remote.voteable import Voteable
from zopache.pages.page import Page    
@implementer (IRSSArticle)
class RSSArticle(Page,Voteable):
    _category = ""
    webClass = "RSSLink"
    emailApproved = True
    publicationApproved = False

    def __init__(self):
        Page.__init__(self)
        importTime=time.time()
        self.importTime = int(importTime)

        
    def preDeleteProcess(self,view):
        #Page.preDeleteProcess(self,view)
        del self.rssFeed.localArticles [self.permaLink]
    
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

    def getImportTime(self,newestArticles):
        while (- self.importTime) in newestArticles:
             self.importTime += 1  
        return self.importTime

    def postAddProcess (self, view = None):
        Page.postAddProcess(self,view = view)
        if "exclusive for subscribers" in self.title.lower():
           self.webApproved = False

        #categories = parentsWhichImplement(self,IRSSCategory)
        #for item in categories:
        #     item.articlesByTime[- importTime] = self

    def getImageURL(self):    
           if hasattr(self,'imageURL'):
               if self.imageURL != "":
                  return self.imageURL
           elif  hasattr(self,'links'):
                for item in self.links:
                    if "image" in item.type:
                        return self.item.href
           return ''
       
    def addImage(self):
           if  'Logo' in self:
               return ''
           imageURL = self.getImageURL()
           if imageURL:
               getImage(imageURL)

