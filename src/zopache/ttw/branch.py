import random
import sys
from zope import schema
from zope import interface
from zope.schema.interfaces import IField
from zope.interface import implementer
from BTrees.OOBTree import OOBTree
from cromlech.browser.interfaces import IPublicationRoot
from zopache.pages.interfaces import IPage
from dolmen.container import IBTreeContainer
from zopache.ttw.interfaces import ICanonical
from dolmen.container import BTreeContainer

from .interfaces import IBranch
from zopache.pages.interfaces import IRootPage
from zopache.ttw.interfaces import IWebClass, IProducts
from zopache.ttw.interfaces import IInternalPrincipal
#from zopache.business.ipolitician import IPolitician

@implementer (IBranch)
class Branch(object):
    branchSize = 0
    def __init__(self):
       self.valuesByToken = OOBTree()
       self.remoteURLs = OOBTree

    def urlOnly(self,link):
       if link.startswith('http'):
          link = link.split('://')[1:]
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
          print (link) 
          print (anObject.__name__)
          print (self.remoteURLs[link].__name__)
          raise Exception (f"""The object called {anObject.__name__} with url: {link} is already in the database. """) 
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
            
    def addItem(self,item):
        self.valuesByToken[item.__name__]= item
       
    def deleteItem(self,item):       
       del self.valuesByToken[item.__name__]       

    def test(self,item):
        if IBTreeContainer.providedBy(item):
           return True
        return False

    def indexTree(self):
        self.valuesByToken=OOBTree()
        self.remoteURLs = OOBTree()
        self.politicians = OOBTree()
        self.indexBranch(self,self)


    def indexBranch(self,tree,branch,itemType=ICanonical):
        for item in branch.values():
            if itemType.providedBy(item):
                self.valuesByToken[item.__name__]=item
            if item.__class__.__name__=='Politician':
                    self.politicians[item.__name__]=item
            if hasattr(item,'remoteURL'):
                self.addRemoteURL(item)
            if IBTreeContainer.providedBy(item):    
                self.indexBranch(tree,item)

    def __contains__(self, key):
        return (key in self._data  or 
                key in self.valuesByToken)

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
             for index in range(1,length):
                 slug = ".".join(words[0:index])
                 context = context.get(slug,object))
                 if context == None:
                     return default
             return context
      
      # IF ALL ELSE FAILS
      return default
    

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


    def __getitem__(self, name):
        """Return the named object, or raise ``KeyError`` if the object
           is not found.
        """
        try:
           return BTreeContainer.__getitem__(self,name)
        except(KeyError):
           return self.valuesByToken[name]


@implementer(IPublicationRoot)       
class Root (Branch):
   pass
