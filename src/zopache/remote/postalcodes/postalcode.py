from zope.interface import implementer
from zopache.pages.page import Page
from zopache.pages.location import Location
from zopache.pages.interfaces import ILocation
from zopache.remote.postalcodes.interfaces import IPostalCode
from zopache.remote.postalcodes.states import stateAbbreviations
from zopache.remote.postalcodes.voter import Voter

prefix = "usa-"

def getPostalContainer(root, postalCode):
        if not postalCode:
           return None
        postalName = prefix + postalCode                   
        postalContainer = root.get(postalName)
        if postalContainer:
           return postalContainer
        else:
            directory = root["usa"]["usa-postal-codes"]
            postalContainer = directory[postalName]
            del directory [postalName]
            shortStateName = postalContainer.state.lower()
            stateSlug = stateAbbreviations[shortStateName]
            state = root [stateSlug]
            state[postalName] = postalContainer
            postalContainer.__parent__ = state      
            return postalContainer


@implementer(IPostalCode)
class PostalCode(Location,Page):
    webClass = "PostalCode"
    webApproved = True

    def __init__(self, postalCode, latitude, longitude,
                 county, city, state):
        Location.__init__(self)    
        self.__name__ = "usa-"+ str(postalCode)
        self.title = postalCode
        self.latitude = latitude
        self.longitude = longitude
        self.county = county
        self.city = city
        self.state = state

    def getMarkerLatLng (self):
               return self.latitude, self.longitude
       
    def getOneMarker(self):
                  lat,lng = self.getMarkerLatLng()
                  aClass = "Z"                  
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
           allZips = root["usa"]["usa-postal-codes"]           
           parent = self.__parent__
           name = self.__name__
           del parent [name]
           self.__parent__ = allZips
           allZips[name] = self
