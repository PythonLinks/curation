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
    def getCompanies(self):
        return self
    
    def getCompaniesRecursively(self,result,showChildren = False):
        return result.append(self)
    #JUST ADD ONE MARKER TO THE LIST                        

             
        
@implementer (ILocationContainer)
class LocationContainer (MapOrLocation):
    icon="ttwicons/Location.svg"    
    def getCompanies(self):
        result=[]
        return self.getCompaniesRecursively(result,showChildren=False)

    def getCompaniesRecursively(self,result, showChildren = None):
        values = self.values()
        for item in values:
            #FOR APPROVED ORGANIZATIONS
            #FOR POLITICIANS, DO IT FIRST
            if not IGeography.providedBy(item):
                continue

            if not item.webApproved:
                continue

            if item.__class__.__name__ in ['OnlineEvent']:
                continue

            if ILocationLeaf.providedBy(item):
                result.append(item)

            elif ILocationContainer.providedBy(item):
                item.getCompaniesRecursively(result,showChildren = True)
                
                #IF ONLY SHOWING CHILDREN
                if item.hasFutureEvent() or showChildren :
                    result.append(item)
            
            elif (IMap.providedBy(item)):
                item.getCompaniesRecursively(result,showChildren = showChildren)
            #FOR A CITY, JUST SHOW ONE ICON    
            elif (ILocation.providedBy(item)):
                result.append(item)

        return result

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

    def getPoints(self):
        if self.showChildren == True:
             mapPoints = self.values()
        else:
             mapPoints = self.getCompanies()
        #if view != None:
        #    mapPoints = self.filter(mapPoints,view)

        for item in mapPoints:
             if not IGeography.providedBy(item):
                   continue
               
             if not item.webApproved:
                    continue
                               
             lat, lng = item.getMarkerLatLng()  
             if ((lat == 0) or
                 lng == 0):
                 continue
             
             # IF LOCATION GET THE JSON
             if ( IGeography.providedBy(item)):
                mapPoints.append(item)
        return mapPoints
     
    def getLocationsJSON(self):
        result = []
        for item in self.mapPoints():
            result.append(item.getOneMarker())
        return json.dumps (result, indent = 2) 

    #ITERATE THROUGH THE CHILDREN
    # IF ONLY ONE COMPANY RETURN IT, ELSE RETURN NONE
    def onlyOneLocationIn(self):
         company=None
         for item in self.values():
             if ILocation.providedBy(item):
                    if (company!=None):
                          return None
                    company=item
         return company          
    

    def getLocations(self):
        values=self.values()
        result=[]
        for item in values:
            if (IGeography.providedBy(item) and 
                item.webApproved):
                result.append(item)
        return result

#So the old maps had a center
#Which was also their Marker
@implementer (ISimpleMap)
class SimpleMap(MapBase):        
    webClass = "SimpleMap"
    def mapPoints(self):
        for item in self.allBlogObjects():
            if IOrganizationBase.providedBy(item):
                yield item

@implementer(IPin)
class Pin(LocationContainer):
    showChildren = False
    remoteURL = ""
    def hasFutureEvent(self):
        return False
