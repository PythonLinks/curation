import time
import os
from dolmen.container import BTreeContainer
from BTrees.OOBTree import OOBTree
from zopache.pages.interfaces import IPage , IRootPage
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

class PageBase(OrderedBTreeContainer,UntrustedHTMLBase,Contained,JsonObject):
    title = ''
    url = ''
    branchSize=1
    description = ''
    webApproved = True    
    # NOT YET SERVING JSON
    def recalculateRootJSON(self):
        pass

    def __init__(self):
         OrderedBTreeContainer.__init__(self)
         self.creationTime=time.time()
         self.modificationTime=time.time()

    def getRoot(self):
         return parentWhichImplements(self,IRootPage)
     
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
            if IWikiPage.providedBy(item):
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
            if IBlogObject.providedBy(item):
                if not item.webApproved:
                   continue
                if ICategory.providedBy(item): 
                    total+=item.countLeaves()
                else:
                    total+=item.branchSize

        self.branchSize=total
        return total


                  
    def hasContent(self):
         if len(self.source)<2 or self.source == NoContentString:
            return False
         else:
            return True
           

    def editDateForRSS(self):
         return time.strftime("%a, %d %b %Y %H:%M:%S %z",time.localtime(self.modificationTime))

    def editDateForSiteMap(self):
         return time.strftime("%Y-%m-%d",time.localtime(self.modificationTime))

    def creationDateForHumans(self):
         return self.creationTime

    def editDateForHumans(self):
         return self.creationTime

    def sortedByTitle(self):
           unsortedList=[]
           for item in self.values():
               if IBlogObject.providedBy(item):
                  unsortedList.append(item)
           aKey=methodcaller('getTitle')
           return sorted(unsortedList, key=aKey)

    def getTitle(self):
         return self.title
     
    def sortedByName(self):
           unsortedList=[]
           for item in self.values():
               if IBlogObject.providedBy(item):
                  unsortedList.append(item)
           aKey=methodcaller('getName')
           return sorted(unsortedList, key=aKey)

    def getName(self):
         return self.__name__

@implementer (IPage)     
class Page(PageBase):
    webClass='WikiPage'        


@implementer(IRootPage)
class RootPage(Branch,PageBase):
    webClass='HomePage'
    def __init__(self):
       Branch.__init__(self)
       PageBase.__init__(self)

    

    
