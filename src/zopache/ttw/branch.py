#FOR INDEXING THIS USES pylons/hypatia.
#Not that well documented.  You may want to read
#https://github.com/repoze/repoze.catalog/blob/master/docs/usage.rst

import time
import random
import sys
from zope import schema
from zope import interface

from hypatia.catalog import Catalog
from hypatia.field import FieldIndex
from hypatia.text import TextIndex
from hypatia.keyword import KeywordIndex

from hypatia.text.htmlsplitter import HTMLWordSplitter

from hypatia.text.lexicon import (
    CaseNormalizer,
    Lexicon,
    Splitter,
    StopWordRemover,
    )

lexicon = Lexicon(
                  HTMLWordSplitter(),
                  Splitter(),
                  CaseNormalizer(),
                  StopWordRemover())

from zope.interface import Interface
from zope.schema.interfaces import IField
from zope.interface import implementer
from BTrees.OOBTree import OOBTree
from BTrees.IOBTree import IOBTree

from cromlech.browser.interfaces import IPublicationRoot
from dolmen.container import BTreeContainer, OrderedBTreeContainer
from dolmen.container import IBTreeContainer

from zopache.pages.interfaces import IPage, IPageBase
from zopache.ttw.interfaces import ICanonical
from zopache.ttw.interfaces import (IBranch,
                                    IWebClass,
                                     IProducts,
                                     IInternalPrincipal)

from zopache.remote.ivideo import IVideo
from zopache.ttw.interfaces import  ICanonical
from zopache.pages.interfaces import ICategory, IImaginary
from zopache.business.interfaces import IOrganization, IOnlineOrganization
from zopache.pages.interfaces import ILocationContainer
from zopache.core.relatives import parentsWhichImplement

#THIS ONE SUBCLASSES OFF OF BTREE CONTAINER
@implementer(IBranch)
class SimpleBranch(object):
    branchSize = 0
    def __init__(self):
       self.valuesByToken = OOBTree()
       
    def addItem(self,item):
        self.indexItem(item,itemType = ICanonical)
        
    def deleteItem(self,item):
       self.unIndexItem(item)

    def indexTree(self):
        self.valuesByToken=OOBTree()
        self.indexBranch(self,self)
        
    def __contains__(self, key):
        return (key in self._data  or 
                key in self.valuesByToken)

    def __delitem__(self, key):
        self.unIndexItem(key)
        BTreeContainer.__delitem__(self,key)
        if key in self.valuesByToken:
                self.valuesByToken.__delitem__(key)
    
    def __getitem__(self, name):
        result = self._data.get(name)
        if result != None:
            return result
        result = self.valuesByToken.get(name)
        if result != None:
            return result
        if name == self.name:
            return self
        return None
    
    def get(self,name,default=None):
      if name in self:
         return self[name]

      if name in self.valuesByToken:
          return self.valuesByToken[name]

      if "." in name:
          words = name.split(".")
          if words[0] in self.valuesByToken:
             context = self
             length = len(words)
             context = self.get(words[0],default = object)
             for index in range(1,length):

                 shortName = words[index]
                 context = context.getImaginary(shortName,default = default)
                 if context == default:
                     return default
             return context
      
      # IF ALL ELSE FAILS
      return default

#THIS ONE SUBCLASSES OFF OF ORDERED CONTAINER  
@implementer (IBranch)
class Branch(SimpleBranch):

    def __init__(self):
        SimpleBranch.__init__(self)
        self.reInit()

    def reInit(self):        
        self.valuesByToken=OOBTree()
        self.remoteURLs = OOBTree()
        self.pagesByTwitterId = OOBTree()
        self.globalArticles = OOBTree()
        self.categoryIndex = IOBTree()
        self.contentByTime = IOBTree()        

        contentCatalog = Catalog()
        contentCatalog['importTime'] = FieldIndex('importTime')
        contentCatalog['isVideo']=FieldIndex('isVideo')
        contentCatalog['recommended']=FieldIndex('recommended')
        contentCatalog['titlePlusDescription']=TextIndex(
                                  'titlePlusDescription',
                                 lexicon = lexicon)

        contentCatalog['ancestorNames']=KeywordIndex('ancestorNames')
        self.contentCatalog = contentCatalog
        
        categoryCatalog = Catalog()
        categoryCatalog['titlePlusDescription']=TextIndex(
                               'titlePlusDescription')
        self.categoryCatalog = categoryCatalog

    @property    
    def nextImportTime(self):    
        lastImportTime = - int  (self.contentByTime.minKey()) 
        currentTime = int(time.time())
        return max (currentTime,lastImportTime + 1)

    def __delitem__(self, key):
        item = self[key]
        self.unIndexItem(item)
        OrderedBTreeContainer.__delitem__(self,key)
                
    def urlOnly(self,link):
       if link.startswith('http'):
          link = link.split('://')[1:]
          #Just to be cautious.
          link =''.join(link)
       return link
   

    def existsRemoteURL(self,link):
       if link == "":
           return False
       link = self.urlOnly(link)
       return self.remoteURLs.get(link,None)
   
    def addRemoteURL(self,anObject):
       link = self.urlOnly(anObject.remoteURL)
       if link == "":
           return

       if link in self.remoteURLs:
          message = f"""The object called {anObject.__name__} with url: {link} is already in the database. """
          raise Exception (message)
       else:
          self.remoteURLs[link] = anObject 
           
    def deleteRemoteURL(self,link):

        if link == "":
           return

        link = self.urlOnly(link)
        del self.remoteURLs[link]
       
    def getUniqueNumberString(self):
        anInteger = random.randint (1,sys.maxsize)        
        while (True):
            if anInteger == sys.maxsize:
                anInteger = 10000
            anInteger += 1
            newName = str(anInteger)
            if not newName in self:
                return newName
            
       
    #def test(self,item):
    #    if IBTreeContainer.providedBy(item):
    #       return True
    #    return False

    def indexTree(self):
        self.reInit()
        self.indexBranch(self,self)
        
    def indexBranch(self,tree,branch,itemType=ICanonical, ancestorNames = tuple()):
        ancestorNames = ancestorNames + (branch.name,)
        
        if IImaginary.providedBy(branch):
            return

        for item in branch.values():
            if itemType.providedBy(item):
                self.indexItem(item,
                               itemType = itemType,
                               ancestorNames = ancestorNames,
                               indexingBranch = True)           
                if IBTreeContainer.providedBy(item):    
                   self.indexBranch(tree,item,ancestorNames = ancestorNames )

    def indexItem(self,item,
                  itemType=ICanonical,
                  ancestorNames = [],
                  indexingBranch = False):

        if not IPageBase.providedBy(item):
            return

        self.valuesByToken[item.__name__] = item
        
        #Unless WebApproved, return.
        if not getattr(item,'webApproved',True):
                   return

        if hasattr(item,'remoteURL'):
            self.addRemoteURL(item)
            
        if hasattr(item,'twitterId'):
            twitterId = item.twitterId
            if twitterId != "":
                self.pagesByTwitterId[twitterId] = item

        if ancestorNames == []:
           if item.parent:
               ancestorNames = item.parent.ancestorNames 

        if ILocationContainer.providedBy(item):
           if indexingBranch:
               item.mapPoints =  OOBTree()
           
        if item.__class__.__name__  == "Category":
           item.reInit()

        elif item.__class__.__name__  == "RSS":
           for category in parentsWhichImplement(item,ICategory):
               category.childFeeds += 1
           #self.categoryCatalog.index_doc(
           #        self.recordCategory(item),
           #        item)               
           
        elif item.__class__.__name__  == "RSSArticle":
            self.contentByTime[ int(item.importTime)] = item
            self.catalogContent(item,ancestorNames)
            self.globalArticles [item.permaLink] = item
                    
        elif item.__class__.__name__ == 'Link': 
            self.contentByTime[int(item.importTime)] = item
            self.catalogContent(item,ancestorNames)
                    
        elif IVideo.providedBy(item):
            self.contentByTime[ int(item.importTime)] = item
            self.catalogContent(item,ancestorNames)            
                    
        elif item.__class__.__name__ =='Politician':
            if (hasattr(item, 'candidateInfo') or
                    hasattr(item, 'electedOfficial')):
               for organization in (
                       parentsWhichImplement(item,ILocationContainer)):
                   organization.mapPoints[item.name] = item
                   
        elif IOrganization.providedBy(item):
            if (item.__class__.__name__ != 'OnlineOrganization'):
               for organization in (
                       parentsWhichImplement(item,ILocationContainer)):
                   organization.mapPoints[item.name] = item
                   
    def catalogContent(self,item,ancestorNames):
        proxy = Proxy(item,ancestorNames)
        self.contentCatalog.index_doc(int(item.importTime),proxy)

    def unCatalogContent(self,item):
        self.contentCatalog.unindex_doc(int(item.importTime))

    def hasAnythingAt(self,importTime):
        result = self.contentCatalog['importTime'].apply((-importTime,-importTime))
        return len(result) 
    
    def unIndexItem(self,item, itemType=IPage):
        if not IPageBase.providedBy(item):
            return
        
        if not item.__name__ in self.valuesByToken: 
           return

        del self.valuesByToken[item.__name__]
       
        if not getattr(item,'webApproved',True): 
                   return

        if hasattr(item,'remoteURL'):
            remoteURL = item.remoteURL
            if remoteURL:
                self.deleteRemoteURL(remoteURL)

        if getattr(item,'twitterId',''):
            del self.pagesByTwitterId [item.twitterId]

        if item.__class__.__name__  == "Category":
           pass 
           #creationTime = int (item.creationTime)
           #del self.categoryIndex[item.creationTime] 
           #self.categoryCatalog.unindex_doc(creationTime)
       
        elif item.__class__.__name__  == "RSS":
           for category in parentsWhichImplement(item,ICategory):
               category.childFeeds -= 1
           #self.categoryCatalog.unindex_doc(item.importTime)           
           #ERROR
           
        elif item.__class__.__name__  == "RSSArticle":
            globalArticles = self.globalArticles
            importTime = int(item.importTime)             
            if importTime in self.contentByTime:
               del self.contentByTime[importTime]
            if item.permaLink in globalArticles:
                del globalArticles [item.permaLink]
            self.unCatalogContent(item)
           
        elif item.__class__.__name__ == 'Link':
            del self.contentByTime[int(item.importTime)]
            self.unCatalogContent(item)
            
        elif IVideo.providedBy(item):
            del self.contentByTime[int(item.importTime)]
            self.unCatalogContent(item)
                        
        elif item.__class__.__name__=='Politician':
            if (hasattr(item, 'candidateInfo') or
                    hasattr(item, 'electedOfficial')):
               for organization in (
                       parentsWhichImplement(item,ILocationContainer)):
                   del organization.mapPoints[item.name]
                   
        elif IOrganization.providedBy(item):
            if (item.__class__.__name__ != 'OnlineOrganization'):
               for organization in (
                       parentsWhichImplement(item,ILocationContainer)):
                   del organization.mapPoints[item.name]                                      
    def checkName(self, name, object):
        """See zope.container.interfaces.INameChooser
        """
        if not name:
            raise ValueError(
                _("An empty name was provided. Names cannot be empty.")
                )

        if name[:1] in '+@' or '/' in name:
            raise ValueError(
                _("Names cannot begin with '+' or '@' or contain '/'")
                )

        if name in self:
            raise KeyError(
                _("The given name is already being used")
                )

        return True


    def chooseName(self, name, object):
        """See zope.container.interfaces.INameChooser
        """

        container = self

        # convert to unicode and remove characters that checkName does not allow

        name = name.replace('/', '-').lstrip('+@')

        if not name:
            name = unicode(object.__class__.__name__)

        # for an existing name, append a number.
        # We should keep client's os.path.extsep (not ours), we assume it's '.'
        dot = name.rfind('.')
        if dot >= 0:
            suffix = name[dot:]
            name = name[:dot]
        else:
            suffix = ''

        nm = name + suffix
        i = 0
        while nm in container:
            i += 1
            nm = name + u'-' + str(i) + suffix

        # Make sure the name is valid.  We may have started with something bad.
        self.checkName(nm, object)

        return nm

#USED TO NOT RECALCULATE ancestorNames EACH TIME.    

from zopache.remote.ivideo import IVideo
class Proxy(object):
    def __init__(self,target,ancestorNames):
        self.target = target
        self.ancestorNames = ancestorNames
    
    @property
    def isArticle(self):
       return self.target.__class__.__name__ in [ "RSSArticle","Link"]

    @property
    def importTime(self):
        importTime = self.target.importTime
        return - int(importTime)        

    @property
    def isVideo(self):
       return IVideo.providedBy(self.target)
   
    @property
    def recommended(self):
        return (IVideo.providedBy(self.target) or
                getattr(self.target,'publicationApproved', False))
                
    def __getattribute__ (self,name):
       if name in {'titlePlusDescription'}:
           return object.__getattribute__(self.target,name)
       else:
          return object.__getattribute__(self,name)
     
@implementer(IPublicationRoot)       
class Root (Branch):
   pass
