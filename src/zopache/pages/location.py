import json

from zope.interface import implementer
from zopache.pages.geo import geoCache
from zopache.pages.cache import cache, PageMixIn, RecentMixIn
from zopache.pages.page import PageBase
from zopache.pages.interfaces  import (IPage,
                                       IPin,
                                       ILocationContainer,
                                       IGeography,
                                       ILocationLeaf,
                                       ILocation,
                                       IMap,
                                       ISimpleMap
                                       )
from zopache.business.interfaces import IOrganizationBase

class MapOrLocation (PageBase):
    webClass = 'Location'
    hidden = False
    def getTitle(self):
        return self.title

    def getMarkerLatLng (self):
           return self.latitude, self.longitude

    def setMarkerLatLng(self, lat,lng):
        self.latitude = lat
        self.longitude = lng
        
    def getOneMarker(self):
                  lat,lng = self.getMarkerLatLng()
                  aClass = self.__class__.__name__[0]                  
                  hasFutureEvent =  str(self.hasFutureEvent())
                  result = [
                      self.__name__,
                      self.title,
                      lat ,
                      lng,
                      aClass,
                      hasFutureEvent]
                  
                  result += self.getOneMarkerCore()
                  result += [ self.remoteURL]
                  return result
              
    #MAY BE OVERRIDDEN BY SUBCLASSES TO GET MORE INFO          
    def getOneMarkerCore(self):
        return []
 

#At least used by events. 
@implementer (ILocationLeaf)
class LocationLeaf (MapOrLocation):
    icon="ttwicons/Location.svg"
    
@implementer (ILocationContainer)
class LocationContainer (MapOrLocation):
    icon="ttwicons/Location.svg"    

@implementer(ILocation)
class Location(LocationContainer):
    pass

import googlemaps
class MapBase(LocationContainer):
    zoomLevel=5.
    mapHeight=0.
    mapWidth=0.
    webClass = 'OpenStreetMap'
    #clientClass = 'Category'
    icon="ttwicons/Map.svg"
    
    def filter(self,mapPoints,view):
        request = view.request
        if not hasattr(request,'form'):
           return mapPoints
        form = request.form
        if not 'focus' in form:
           return mapPoints
        value = form ['focus']
        if value in ['', 'None']:
           return mapPoints
        result = []
        for item in mapPoints:
               if not hasattr(item,'focus'):
                  result.append(item)
                  continue
               if item.focus == value:
                  result.append(item)
        return result          

     
    def getLocationsJSON(self):
        result = []
        for item in self.mapPoints.values():
            result.append(item.getOneMarker())
        return json.dumps (result, indent = 2) 

#So the old maps had a center
#Which was also their Marker
@implementer (ISimpleMap)
class SimpleMap(MapBase):        
    webClass = "SimpleMap"

@implementer(IPin)
class Pin(LocationContainer):
    showChildren = False
    remoteURL = ""
    def hasFutureEvent(self):
        return False
