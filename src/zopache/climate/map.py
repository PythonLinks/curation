
from zopache.pages.location import Map
from zopache.pages.interfaces import IMap
from zope.interface import implementer

@implementer(IMap)
class StrikeMap(Map):
    webClass = "ClimateStrikeMap"
