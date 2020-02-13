from zopache.business.interfaces import IMap, ICompanyOrOrganization
from zope.interface import implementer
from zopache.pages.location import MapBase
from zopache.categories.category import Category

@implementer (IMap)
class Map  (Category,MapBase):
    webClass = "OpenStreetMap"
    hidden = False
    interface = IMap
    

        
