from zopache.business.interfaces import IMap, ICompanyOrOrganization
from zope.interface import implementer
from zopache.pages.location import MapBase
from zopache.pages.page import Page
from zopache.business.subscribe import Member
from zopache.business.interfaces import ICity
from zopache.pages.location import LocationContainer
from zopache.business.company import GeoBase

@implementer(ICity)
class City(GeoBase,LocationContainer):
    def getCompaniesRecursively(self,result,showChildren = False):
        return result.append(self)

@implementer (IMap)
class Map  (Page,MapBase,Member):
    webClass = "OpenStreetMap"
    hidden = False
    interface = IMap
    def __init__(self):
        Member.__init__(self)
        Page.__init__(self)    
        
