
from .interfaces import IMap
from zope.interface import implementer
from zopache.pages.location import MapBase
from zopache.categories.category import Category

@implementer (IMap)
class Map  (Category,MapBase):
    webClass = "GoogleMap"
    hidden = False

    
        
