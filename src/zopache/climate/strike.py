from zopache.pages.location import Location
from zopache.pages.location import Location
from zopache.pages.interfaces import ILocation
from zope.interface import implementer

@implementer(ILocation)
class ClimateStrike (Location):
    webClass = "ClimateStrike"
