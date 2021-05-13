import time
import os
import datetime
from pydoc import locate
from operator import methodcaller
from dolmen.container import BTreeContainer
from BTrees.OOBTree import OOBTree
from zopache.pages.interfaces import (ITime,IContent,IPage ,
                                      IRootPage, ISiteRootPage, INews)
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
from zopache.application.allblogobjects import ProcessTree, AllBlogObjects
from collections import defaultdict
from zopache.core.interfaces import ICountable
from cromlech.security import unauthenticated_principal as Anonymous
from zopache.pages.interfaces import ILink,IActionNetwork
from zopache.ttw.branch import Branch

class PageVeryBase(AllObjects,OrderedBTreeContainer,UntrustedHTMLBase,Contained,ProcessTree):
    private = False
    branchSize=1
    webApproved = True
    emailApproved = False
    basePath = "/"
    createdBy = None
    editedBy = None

    
    def className(self):
        return self.__class__.__name__
    
    def getTitleFor(self,view):
        return self.title
    
    def getDescriptionFor(self,view):
        return self.description

    def countMe (self):
        if not self.webApproved:
            return False
        if (ICountable.providedBy(self) or
             len (self.source) > 5):
            return True
        return False

    def countLeaves(self):
        total=0
        if self.countMe():   
            total += 1        
        for item in self.realChildCategories():
            if IPage.providedBy(item):
                    total+=item.countLeaves()
        self.branchSize=total
        return total    
    
    def getDefaultThumbNailURL(self):
        if 'Logo' in self:
            return  self.shortURL (self,viewName ='Logo')
        return ""

    def sortByClass(self):
        result = defaultdict(list)   
        for item in self.values():
            result[item.__class__.__name__].append(item)
        return result    

    
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

                              
    def allPagesAsList(self):
        pages = []
        for item in AllBlogObjects(self):
            pages.append(item)
        return pages
    
    #USED TO DISPLAY CHILDREN, BUT NOT HTML OBJECTS
    def childCategories(self):
        result =[]
        for item in self.values():
            if (IPage.providedBy (item) and item.webApproved):
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
       
    def postProcessCore(self,view=None):
        self.partialPostProcess(view=view)
        self.recalculateRootJSON()
        cache.resetCache(self)

    def preProcess(self,view=None):
        siteRoot = view.getSiteRoot()
        if self.webApproved:
            siteRoot.unIndexItem(self)
        
    def postProcess(self,view=None):
        siteRoot = view.getSiteRoot()
        siteRoot.indexItem(self)        
        self.modificationTime=time.time()        
        self.postProcessCore(view = view)
        principal = view.request.principal
        if principal != Anonymous:
           name = view.request.principal.__name__
           try:
              name = int(name)
           except:
              pass
           self.editedBy = name
            
    def postAddProcess(self,view=None):
        self.postProcessCore(view=view)        
        principal = view.request.principal
        if principal != Anonymous:
           name = view.request.principal.__name__
           try:
              name = int(name)
           except:
              pass
           self.createdBy = name
        
        if ((self.__parent__ != None) and
            self.__parent__.private):
            self.private = True
            
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

    def __delitem__(self,key):
        siteRoot = self.getSiteRoot()
        item = self[key]
        siteRoot.unIndexItem(item)
        OrderedBTreeContainer.__delitem__(self,key)
        
    def __setitem__(self,  key,item):
        OrderedBTreeContainer.__setitem__(self,key,item)
        if IPage.providedBy(item):
           siteRoot = self.getSiteRoot()     
           siteRoot.addItem(item)
                  
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

    def sortedByName(self):
           unsortedList=[]
           for item in self.values():
               if IPage.providedBy(item):
                  unsortedList.append(item)
           aKey=methodcaller('getName')
           return sorted(unsortedList, key=aKey)

    def getName(self):
         return self.__name__
     
    def allValues(self):
        return self.values()

class PageBase(PageVeryBase,JsonObject):
    title = ''
    description = ''
    source = ''

    def sortedByTitle(self):
           unsortedList=[]
           for item in self.values():
               if IPage.providedBy(item):
                  unsortedList.append(item)
           aKey=methodcaller('getTitle')
           return sorted(unsortedList, key=aKey)

    
    def partialPostProcess(self, view=None):        
        self.description=self.description.replace ('"' , "&ldquo;", 1)
        self.description=self.description.replace ('"' , "&rdquo;", 1)
        self.description=self.description.replace ('"' , "&ldquo;")
        self.description=self.description.replace ('\n' , " ")
        self.description=self.description.replace ('\r' , " ")                

        self.title=self.title.replace ('"' , "&ldquo;", 1)
        self.title=self.title.replace ('"' , "&rdquo;", 1)
        self.title=self.title.replace ('"' , "&ldquo;")
        self.title=self.title.replace ('\n' , " ")
        self.title=self.title.replace ('\r' , " ")                

    
    def getTitle(self):
         return self.title

    def getTitleForDomain(self,domain):
        return self.title

    def getDescriptionForDomain(self,domain):
        return self.description

@implementer (IActionNetwork)
class ActionNetwork(PageBase, PageMixIn):
    webClass='Action'
    icon="ttwicons/WikiPage.png"
    
@implementer (IPage)     
class Page(PageBase, PageMixIn):
    webClass='WikiPage'
    icon="ttwicons/WikiPage.png"


@implementer (ILink)     
class Link(PageBase, PageMixIn):
    webClass='Link'
    icon="ttwicons/WikiPage.png"

@implementer (INews)     
class News (Page,RecentMixIn):
    webClass = 'NewsItem'
    pass

from zopache.pages.interfaces import ISiteRoot
from zopache.pages.cache import Cache
@implementer(ISiteRoot)
class SiteRoot(Branch,PageBase,PageMixIn):
    webClass='HomePage'
    homePage = ''
    
    def preProcess(self,view=None):
        pass
        
    def __init__(self):
       Branch.__init__(self)
       PageBase.__init__(self)
       cache = Cache()

    def setJson(self):
         self.json=self.jsonTree(0)

         
@implementer(IRootPage)         
class RootPage(SiteRoot):
    def getSiteRootFor(self,hostName):
        return self

@implementer(ISiteRootPage)         
class SiteRootPage(SiteRoot):
    def __init__(self):
       Branch.__init__(self)
       Page.__init__(self)
       
       #NOT SURE WHY THIS COULD NOT BE AT THE TOP OF THE PAGE
       from zopache.ttw.principalfolder import PrincipalFolder
       self ["person"] = PrincipalFolder()
        
    def getSiteRootFor(self,hostName):
        return self    
