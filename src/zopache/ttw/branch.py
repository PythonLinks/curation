from zope import schema
from zope import interface
from zope.schema.interfaces import IField
from zope.interface import implementer
from BTrees.OOBTree import OOBTree
from cromlech.browser.interfaces import IPublicationRoot
from zopache.pages.interfaces import IPage
from dolmen.container import IBTreeContainer

from dolmen.container import BTreeContainer

from .interfaces import IBranch
from zopache.core.breadcrumbs import Breadcrumbs


@implementer (IBranch)
class Branch(object):
    def __init__(self):
       self.valuesByToken = OOBTree()
       #self.tokensByValue = {}

    def indexTree(self):
        self.valuesByToken=OOBTree()
        #self.tokensByValue={}
        self.indexBranch(self,self)
        #self._p_changed=True

    def test(self,item):
        if IBTreeContainer.providedBy(item):
           return True
        return False
        
    def indexBranch(self,tree,branch):
        for item in branch.values():
               #allow any zclass object
               # and item.__ZClass__.__name__=='Skill':
               if IPage.providedBy(item):
                   #self.tokensByValue[item]=item.__name__
                   self.valuesByToken[item.__name__]=item
                   self.indexBranch(tree,item)



    def __contains__(self, key):
        return (key in self._data  or 
                key in self.valuesByToken)

    def get(self,name,default=None):
      if name in self:
         return self[name]

      if name in self.valuesByToken:
          return self.valuesByToken[name]

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
