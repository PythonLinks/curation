from dolmen.container import BTreeContainer

from zopache.ttw.html import UntrustedHTMLBase
from zopache.core.ancestors import Ancestors
from zopache.core.uniquename import UniqueName
from zopache.core.ancestors import Ancestors
from zopache.core import Container
from zopache.pages.used import Used

class Source(Container, 
             Used,
             UniqueName,
             Ancestors,
             UntrustedHTMLBase):    
            
    def __init__(self):
        Container.__init__(self)
        
    def __delitem__(self,key):
        siteRoot = self.getPublicationRoot()
        item = self[key]
        siteRoot.unIndexItem(item)
        BTreeContainer.__delitem__(self,key)
        
    def __setitem__(self,  key,item):
        BTreeContainer.__setitem__(self,key,item)
        siteRoot = self.getPublicationRoot()     
        siteRoot.addItem(item)
        
