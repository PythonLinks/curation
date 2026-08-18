from slugify import slugify

from zope.interface import implementer

from zopache.pages.page import Page
from zopache.pages.location import Location
from zopache.remote.postalcodes.interfaces import IPostalCountryCode

@implementer(IPostalCountryCode)
class PostalCountryCode(Location,Page):
    webClass = "PostalCountryCode"
    webApproved = True

    def __init__(self, countryCode, postalCode, countryName,latitude, longitude):
        Location.__init__(self)    
        self.__name__ = slugify(countryCode +  '_' + postalCode)
        self.postalCode = postalCode
        self.latitude = latitude
        self.longitude = longitude
        self.countryCode = countryCode
        self.countryName = countryName        

    @property
    def title(self):
            return self.country + " " + self.postalCode
    
    def getMarkerLatLng (self):
        return self.latitude, self.longitude
       
    def getOneMarker(self):
        lat,lng = self.getMarkerLatLng()
        aClass = "P"  #Type of object. P for person. 
        hasFutureEvent =  self.hasFutureEvent()
        result = [
            self.__name__,
            self.title,
            lat ,
            lng,
            aClass,
            hasFutureEvent]
        result += [ self.remoteURL]
        result += [len(self)]
        return result
              

    @property
    def remoteURL(self):
            return ""
    
    def hasFutureEvent(self):
        return 0
    
    def canView(self,view):
        return True

    def __delitem__(self,key):
        Page.__delitem__(self,key)
        if len (self) == 0:
           root = self.getPublicationRoot()
           root.unindex(self)
           parent = self.__parent__
           name = self.__name__
           del parent [name]
