from zopache.business.company import GeoBase
from zopache.business.geocoding import Address
from zopache.pages.location import LocationLeaf
from zopache.business.ipolitician import IPolitician, IAddPolitician
from zopache.pages.page import SiteRoot

@implementer (IPolitician)
class Politician (GeoBase,LocationLeaf):
    webClass = "Politician"
    clientClass = "category"
    def preDeleteProcess(self,view):
        siteRoot = self.getSiteRoot()
        del siteRoot[self.__name__
        LocationLeaf.preDeleteProcess(self,view)
            
@implementer (IPoliticiansSite)
class PoliticiansSite (GeoBase,LocationLeaf,SiteRoot):
    webClass = "Politician"
    clientClass = "category"    
    def __init__(self):
        SiteRoot.__init__(self)
        GeoBase.__init__(self)
        LocationLeaf.__init__(self)
