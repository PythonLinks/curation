import time
import os
import datetime
from pydoc import locate
from operator import methodcaller
from dolmen.container import BTreeContainer
from BTrees.OOBTree import OOBTree
from zopache.pages.interfaces import ITime,IContent,IPage , IRootPage, INews
from zopache.core.getroot import getSiteRoot, getZodbRoot
from zopache.ttw.html import UntrustedHTMLBase
from dolmen.container import OrderedBTreeContainer
from cromlech.container.contained import Contained
from zope.interface import implementer
from zopache.ttw.interfaces import IBranch
from zopache.ttw.branch import Branch
from zopache.core.relatives import parentWhichImplements
from zopache.core.relatives import parentsUpTo
from zopache.pages.jsonobject import JsonObject
from zopache.pages.cache import cache, PageMixIn, RecentMixIn
from zopache.core import AllObjects
from zopache.pages.allblogobjects import ProcessTree, AllBlogObjects

class PageBase(AllObjects,OrderedBTreeContainer,UntrustedHTMLBase,Contained,JsonObject,ProcessTree):
    title = ''
    url = ''
    source = ''
    branchSize=1
    description = ''
    webApproved = True
    emailApproved = False
    
    def getDefaultThumbNailURL(self):
        if 'Logo' in self:
            return  self.shortURL (self,viewName ='Logo')
        return ""
    
    def moveURL(self):
        if hasattr(self,'url'):
           self.remoteURL = self.url
           del self.url
           
    def listFutureEvents(self):
        result = []
        for item in self.allBlogObjects():
            if (ITime.providedBy (item)):
                now = datetime.datetime.now()
                if now < item.time: 
                   result.append(item)
        return result

    def hasFutureEvent(self):
        result = 0
        for item in self.childCategories():
            if (ITime.providedBy (item)):
                now = datetime.datetime.now()
                if item.time == None:
                   continue
                if now < item.time: 
                   result +=1
        return result
                              
    def allPagesAsList(self):
        pages = []
        for item in AllBlogObjects(self):
            pages.append(item)
        return pages
    
    #USED TO DISPLAY CHILDREN, BUT NOT HTML OBJECTS
    def childCategories(self):
        result =[]
        for item in self.values():
            if IPage.providedBy (item):
               result.append (item)
        return result
    
    def canView(self,view):
        return True
    
    def allValuesAsList(self):
        result = []
        for item in self.values():
               result.append (item)
        return result
    
    def valuesAsList(self):
        result = []
        for item in self.values():
            if IContent.providedBy(item):            
               result.append (item)
        return result

    def listOfAClass(self,aClassName):
        result = []
        for item in self.values():
            if (item.__class__.__name__ == aClassName):
               result.append (item)
        return result

    def listOfAClassInParents(self,aClassName):
        result = []
        node = self
        while node != None:
            for item in node.values():
                if (item.__class__.__name__ == aClassName):
                   result.append (item)
            if not hasattr(node,'__parent__'):
               break
            node = node.__parent__
        result.reverse()    
        return result

        
    def listOfAnInterface(self,aDottedName):
        result = []
        theInterface = locate(aDottedName)        
        if theInterface == None:
            return result
        for item in self.values():
            if theInterface.providedBy(item): 
               result.append (item)
        return result
    
    def getClientClass(self):
        if (hasattr(self,'clientClass') and
           self.clientClass != ""):
           return self.clientClass
        else:
           return self.webClass
       
    def postProcess(self,view=None):
        self.partialPostProcess(view=view)
        self.recalculateRootJSON()
        cache.resetCache(self)
        
    def partialPostProcess(self, view=None):        
        self.description=self.description.replace ('"' , "&ldquo;", 1)
        self.description=self.description.replace ('"' , "&rdquo;", 1)
        self.description=self.description.replace ('"' , "&ldquo;")
        self.description=self.description.replace ('\n' , " ")        

        self.title=self.title.replace ('"' , "&ldquo;", 1)
        self.title=self.title.replace ('"' , "&rdquo;", 1)
        self.title=self.title.replace ('"' , "&ldquo;")
        self.title=self.title.replace ('\n' , " ")        
        
    def postAddProcess(self,view=None):
        self.postProcess(view=view)
        if not view.treeSecurity():
           view.notifyAdminsNewPage()

    def recalculateRootJSON(self):
         jsonRoot = self.getSiteRoot()
         if jsonRoot:
            jsonRoot.setJson()
    
    def __init__(self):
         OrderedBTreeContainer.__init__(self)
         self.creationTime=time.time()
         self.modificationTime=time.time()

    def getSiteRoot(self):
        return getSiteRoot(self)

    def getZodbRoot(self):
        return getZodbRoot (self)

     
    def blogParents(self):
         return parentsUpTo(self,IRootPage)

    def isCategory (self):
        return False
    
    def isVideo(self):
        return False

    def isPage (self):
        return True    

    def wikiPageChildren(self):
        for item in self.values():
            if IPage.providedBy(item):
                yield item                   

    def __setitem__(self,  key,item):
        OrderedBTreeContainer.__setitem__(self,key,item)
        if IPage.providedBy(item):
           valuesByToken=self.parentBranch().valuesByToken
           valuesByToken[key]=item     
        
    def parentBranch(self):
        return parentWhichImplements(self,IBranch)

    #COUNTS ALL NODES           
    def countLeaves(self):
        total=1
        for item in self.values():
            if IPage.providedBy(item):
                if not item.webApproved:
                   continue
                if IPage.providedBy(item): 
                    total+=item.countLeaves()
                else:
                    total+=item.branchSize

        self.branchSize=total
        return total


                  
    def hasContent(self):
         if len(self.source)<2:
            return False
         else:
            return True
           

    def editDateForRSS(self):
         return time.strftime("%a, %d %b %Y %H:%M:%S %z",time.localtime(self.modificationTime))

    def editDateForSiteMap(self):
         return time.strftime("%Y-%m-%d",time.localtime(self.modificationTime))

    def creationDateForHumans(self):
         return time.strftime("%Y-%m-%d",time.localtime(self.creationTime))

    def editDateForHumans(self):
         return self.creationTime

    def sortedByTitle(self):
           unsortedList=[]
           for item in self.values():
               if IPage.providedBy(item):
                  unsortedList.append(item)
           aKey=methodcaller('getTitle')
           return sorted(unsortedList, key=aKey)

    def getTitle(self):
         return self.title
     
    def sortedByName(self):
           unsortedList=[]
           for item in self.values():
               if IPage.providedBy(item):
                  unsortedList.append(item)
           aKey=methodcaller('getName')
           return sorted(unsortedList, key=aKey)

    def getName(self):
         return self.__name__
     
    def preDeleteProcess(self,view):
        if hasattr(self,'remoteURL'):
            siteRoot = self.getSiteRoot()
            del siteRoot.remoteLinks [self.remoteURL]
    
@implementer (IPage)     
class Page(PageBase, PageMixIn):
    webClass='WikiPage'
    icon="ttwicons/WikiPage.png"
    
from cromlech.security import unauthenticated_principal as Anonymous
from zopache.pages.interfaces import ILink    
@implementer (ILink)     
class Link(PageBase, PageMixIn):
    webClass='Link'
    icon="ttwicons/WikiPage.png"
    def postAddProcess(self,view=None):
        siteRoot = self.getSiteRoot()
        siteRoot.valuesByToken[self.__name__] = self
        principal = view.request.principal
        if principal != Anonymous:
           self.createdBy = view.request.principal.__name__
        PageBase.postAddProcess(self, view=view)
        #The Following is not needed.
        #PageMixIn.postAddProcess(self, view=view)       
    
@implementer (INews)     
class News (Page,RecentMixIn):
    webClass = 'NewsItem'
    pass

from zopache.pages.cache import Cache
@implementer(IRootPage)
class RootPage(Branch,PageBase,PageMixIn):
    webClass='HomePage'
    homePage = ''
    
    def __init__(self):
       Branch.__init__(self)
       PageBase.__init__(self)
       cache = Cache()
       
    def setJson(self):
        pass

    
