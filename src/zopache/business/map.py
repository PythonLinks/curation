from zopache.business.interfaces import IMap
from zope.interface import implementer
from zopache.pages.location import MapBase
from zopache.pages.page import Page
from zopache.business.interfaces import ICity
from zopache.pages.location import LocationContainer
from zopache.business.geocoding import GeoBase

@implementer(ICity)
class City(GeoBase,LocationContainer):
    def getCompaniesRecursively(self,result,showChildren = False):
        return result.append(self)

@implementer (IMap)
class Map  (Page,MapBase):
    webClass = "OpenStreetMap"
    hidden = False
    interface = IMap
        
