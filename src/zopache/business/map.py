from zopache.business.interfaces import IMap, ICompanyOrOrganization
from zope.interface import implementer
from zopache.pages.location import MapBase
from zopache.pages.page import Page

@implementer (IMap)
class Map  (Page,MapBase):
    webClass = "OpenStreetMap"
    hidden = False
    interface = IMap
    

        
