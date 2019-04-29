
from .interfaces import ICompany
from zopache.pages.page import PageBase
from zopache.pages.interfaces import IPage , IRootPage
from zope.interface import implementer
from .geo import geoCache
from zopache.pages.cache import cache, PageMixIn, RecentMixIn


@implementer (ICompany)
class Company  (Location):
    pass

    
        
