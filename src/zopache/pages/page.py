import time
import os
import datetime

from operator import methodcaller
from dolmen.container import BTreeContainer
from BTrees.OOBTree import OOBTree
from zopache.pages.interfaces import IContent,IPage , IRootPage, INews
from zopache.core.getroot import getSiteRoot, getZodbRoot
from zopache.ttw.html import UntrustedHTMLBase
from dolmen.container import OrderedBTreeContainer
from zopache.core.breadcrumbs import parentWhichImplements
from cromlech.container.contained import Contained
from zope.interface import implementer
from zopache.ttw.interfaces import IBranch
from zopache.ttw.branch import Branch
from zopache.core.breadcrumbs import parentWhichImplements
from zopache.core.breadcrumbs import parentsUpTo
from zopache.pages.jsonobject import JsonObject
from zopache.pages.cache import cache, PageMixIn, RecentMixIn
from zopache.core import AllObjects
from zopache.pages.allblogobjects import AllBlogObjects
from zopache.business.interfaces import IEvent

class PageBase(AllObjects,OrderedBTreeContainer,UntrustedHTMLBase,Contained,JsonObject):
    title = ''
    url = ''
    branchSize=1
    description = ''
    webApproved = True
    
    def allBlogObjects(self):
        return AllBlogObjects(self)

    def allTreeObjects(self):
        return AllBlogObjects(self)        

    def listFutureEvents(self):
        result = []
        for item in self.allBlogObjects():
            if (IEvent.providedBy (item)):
                now = datetime.datetime.now()
                if now < item.time: 
                   result.append(item)
        return result

    def hasFutureEvent(self):
        for item in self.allBlogObjects():
            if (IEvent.providedBy (item)):
                now = datetime.datetime.now()
                if now < item.time: 
                   return True
        return False
                              
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
    
    def canView(self):
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


    def getClientClass(self):
        if (hasattr(self,'clientClass') and
           self.clientClass != ""):
           return self.clientClass
        else:
           return self.webClass
       
    def postProcess(self,view=None):

        self.recalculateRootJSON()
        cache.resetCache(self)
        self.description=self.description.replace ('"' , "'")
        self.description=self.description.replace ('\n' , " ")        
        
    def postAddProcess(self,view=None):
        self.postProcess(view=view)
        view.notifyAdminsNewPage()
        
    # NOT YET SERVING JSON
    def recalculateRootJSON(self):
        pass

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
        pass
    
@implementer (IPage)     
class Page(PageBase, PageMixIn):
    webClass='WikiPage'
    icon="ttwicons/WikiPage.png"

from zopache.pages.interfaces import ILink    
@implementer (ILink)     
class Link(PageBase, PageMixIn):
    webClass='Link'
    icon="ttwicons/WikiPage.png"

    
@implementer (INews)     
class News (Page,RecentMixIn):
    webClass = 'News'
    pass

from zopache.pages.cache import Cache
@implementer(IRootPage)
class RootPage(Branch,PageBase,PageMixIn):
    webClass='HomePage'
    def __init__(self):
       Branch.__init__(self)
       PageBase.__init__(self)
       cache = Cache()
    

    
