from zope.interface import implementer

from dolmen.container import IBTreeContainer

from zopache.business.company import GeoBase
from zopache.pages.location import LocationLeaf
from zopache.business.ipolitician import (IPolitician,
                                          IAddPolitician,
                                          IPoliticiansSite)
from zopache.pages.page import SiteRoot
from zopache.business.region import Region
from zopache.pages.interfaces import IPage
from zopache.business.imaginarypage import ImaginaryPage
    

@implementer (IPolitician)
class Politician (ImaginaryPage,GeoBase,LocationLeaf):
    localOrNational = ""
    webClass = "Politician"
    clientClass = "category"
   

@implementer (IPoliticiansSite)
class PoliticiansSite (GeoBase,LocationLeaf,SiteRoot):
    webClass = "Politician"
    clientClass = "category"    
    def __init__(self):
        SiteRoot.__init__(self)
        GeoBase.__init__(self)
        LocationLeaf.__init__(self)

