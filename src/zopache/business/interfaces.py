from zope.interface import Interface
from zopache.pages.interfaces import ILocation
from zopache.pages.interfaces import ILocation as IMapBase

class ICompany (ILocation):
    pass

class IMap (IMapBase):
    pass
