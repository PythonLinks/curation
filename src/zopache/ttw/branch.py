import random
import sys
from zope import schema
from zope import interface
from zope.interface import Interface
from zope.schema.interfaces import IField
from zope.interface import implementer
from BTrees.LOBTree import  LOTreeSet
from BTrees.OOBTree import OOBTree



from cromlech.browser.interfaces import IPublicationRoot
from zopache.pages.interfaces import IPage
from dolmen.container import IBTreeContainer
from zopache.ttw.interfaces import ICanonical
from dolmen.container import BTreeContainer, OrderedBTreeContainer

from .interfaces import IBranch
from zopache.pages.interfaces import IRootPage, IPage
from zopache.ttw.interfaces import IWebClass, IProducts
from zopache.ttw.interfaces import IInternalPrincipal
#from zopache.business.ipolitician import IPolitician
from zopache.pages.interfaces import IImaginary
from zopache.ttw.interfaces import  ICanonical
from BTrees.LOBTree import  LOTreeSet

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
       self.valuesByToken = OOBTree()
       self.remoteURLs = OOBTree
       self.politicians = OOBTree()
       self.pagesByTwitterId = OOBTree()
       self.socialNodeByTwitterId = OOBTree()
       self.globalArticles = OOBTree()
       self.newestArticles = OOBTree()
       self.newestLinks = OOBTree()       
       self.approvedArticles = OOBTree()       
       self.remoteArticles = OOBTree()
       
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
            
       
    def test(self,item):
        if IBTreeContainer.providedBy(item):
           return True
        return False

    def indexTree(self):

        
        self.valuesByToken=OOBTree()
        self.remoteURLs = OOBTree()
        self.politicians = OOBTree()
        self.pagesByTwitterId = OOBTree()
        self.socialNodeByTwitterId = OOBTree()
        self.globalArticles = OOBTree()
        self.newestArticles = OOBTree()
        self.newestLinks = OOBTree()        
        self.approvedArticles = OOBTree()        
        self.remoteArticles = OOBTree()                
        self.indexBranch(self,self)


    def indexBranch(self,tree,branch,itemType=ICanonical):
        
        if IImaginary.providedBy(branch):
            return

        for item in branch.values():
            print ( itemType.providedBy(item),item.__name__)            
            if itemType.providedBy(item):
                self.indexItem(item, itemType = itemType)           
                if IBTreeContainer.providedBy(item):    
                   self.indexBranch(tree,item)

    def indexItem(self,item, itemType=ICanonical):
        if not IPage.providedBy(item):
            return
        self.valuesByToken[item.__name__] = item
        
        if item.__class__.__name__  == "RSSArticle":
            self.globalArticles [item.permaLink] = item
            
        if (hasattr(item,'webApproved') and
                   not item.webApproved ):
                   return
               
        if hasattr(item,'remoteURL'):
            self.addRemoteURL(item)
            
        if hasattr(item,'twitterId'):
            twitterId = item.twitterId
            if twitterId != "":
                self.pagesByTwitterId[twitterId] = item
                
        if item.__class__.__name__ in [ "SocialNode"]:
            for node in item.allNodes():
                twitterId= node.twitterId
                if twitterId:
                    self.socialNodeByTwitterId[twitterId] = item
                    
        if item.__class__.__name__  == "RSSArticle":
            time = item.importTime

            if item.publicationApproved:
                self.approvedArticles [-time] = item
            else:
                self.newestArticles[-time] = item
            
        if item.__class__.__name__ =='Politician':
            if (hasattr(item, 'candidateInfo') or
                    hasattr(item, 'electedOfficial') or                    
                    hasattr(item, 'partyOfficer')):
                    self.politicians[item.__name__]=item
                    
        if item.__class__.__name__ == 'Link':
             self.newestLinks [-item.creationTime] = item

    def hasArticle(self,importTime):
        importTime = - importTime
        ((importTime in self.newestArticles) or
        (importTime in self.approvedArticles))
        
    def unIndexItem(self,item, itemType=IPage):
        if not IPage.providedBy(item):
            return        
        if not item.__name__ in self.valuesByToken: 
           return

        del self.valuesByToken[item.__name__]
        
        if (hasattr(item,'webApproved') and
                   not item.webApproved ):
                   return
       
        if hasattr(item,'remoteURL'):
            remoteURL = item.remoteURL
            if remoteURL:
                self.deleteRemoteURL(remoteURL)
                
        if item.__class__.__name__ == "RSSArticle":
            if item.permaLink in self.globalArticles:
                del self.globalArticles [item.permaLink]
            importTime = -item.importTime
            newestArticles = self.newestArticles
            if importTime in newestArticles:
               del newestArticles [importTime]
               
            approvedArticles = self.approvedArticles   
            if importTime in approvedArticles:   
               del approvedArticles [importTime]
            
        if item.__class__.__name__ == "Link":
            del self.newestLinks [-item.creationTime]            

        
        if hasattr(item,'twitterId'):
            twitterId = item.twitterId            
            if twitterId:
                del self.pagesByTwitterId [twitterId]

        if item.__class__.__name__ in [ "SocialNode"]:
            for node in item.allNodes():
                twitterId = node.twitterId
                if twitterId:
                   if twitterId in self.socialNodeByTwitterId:  
                       del self.socialNodeByTwitterId[node.twitterId] 
                                                     
        if item.__class__.__name__=='Politician':
            if (hasattr(item, 'candidateInfo') or
                    hasattr(item, 'electedOfficial') or                    
                    hasattr(item, 'partyOfficer')):
                    del self.politicians[item.__name__]
                    

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



@implementer(IPublicationRoot)       
class Root (Branch):
   pass
