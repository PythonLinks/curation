import time
from zope.interface import Interface
from zope import schema
from zopache.pages.interfaces import IPage
from zopache.pages.page import Page
from zopache.core.viewdecorators import *
from zopache.remote.interfaces import IVoteable
from zopache.crud.getimage import createImageInFrom
from webpreview import web_preview

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
    imageURL = ""
    webClass = "RSSLink"
    emailApproved = True
    publicationApproved = False

    def __init__(self):
        importTime=time.time()
        importTime = int(sortTime)
        self.importTime = sortTime
        
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

    def getImportTime(self,siteRoot):
        uniqueTime = siteRoot.uniqueTime
        while (- self.importTime) in uniqueTime:
             self.sortTime += 1  
        return self.sortTime

    def postAddProcess (self, view = None):
        Page.postAddProcess(self,view = view)
        if "exclusive for subscribers" in self.title.lower():
           self.webApproved = False

        #categories = parentsWhichImplement(self,IRSSCategory)
        #for item in categories:
        #     item.articlesByTime[- sortTime] = self

        
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

    async def processResponse(self,response,view):

        if self.getImageURL():
           print ("Fetching  Image " + self.parent.name + " " +self.name) 
           content = await response.read()
           return self, content, response
        else:
            print ("Fetching Page " + self.name)             
            html  =  await response.text()
            result = web_preview(self.articleURL, content = html, parser="html.parser")
            imageURL = result [2]
            print (result)
            breakpoint()            

            print ("HERE is the IMAGE URL ", imageURL)
            return None
            #if imageURL != "":
            #   self.imageURL = imageURL 
            #   print ("Found IMAGE URL", self.imageURL)
            #   return await fetch(self,5, time.time(),view)
