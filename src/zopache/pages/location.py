
from .interfaces import ILocation,IMap
from zope.interface import implementer
from .geo import geoCache
from zopache.pages.cache import cache, PageMixIn, RecentMixIn
#from zopache.business.interfaces import IMap, ICompanyOrOrganization
from zopache.pages.page import PageBase
from zopache.pages.interfaces import IPage , IRootPage
from zopache.pages.interfaces  import (ILocationContainer,
                                       ILocationOrMap,
                                       ILocationLeaf)

class MapOrLocation (PageBase):
    latitude = 45.
    longitude = 0.
    webClass = 'Location'
    specialization = ''
    showChildren = True
    
    def getTitle(self):
        return self.title
    
    #JUST ADD ONE MARKER TO THE LIST                        
    def getOneMarker(self, firstItem, result):
                  if not hasattr(self, 'longitude'):
                      return result,firstItem
                  if not firstItem:
                     result +=','
                  firstItem=False      
                  result+='\n'
                  result += '['
                  result +='"' +  self.__name__ + '"'
                  result += ','
                  result +='"' +  self.getTitle() + '"'
                  result += ','
                  lat,lng = self.getMarkerLatLng()
                  result +=  str(lat)  
                  result += ','    
                  result += str(lng)
                  color = self.getColor()
                  result += ",'" + color +"'"
                  result += "," + str(self.hasFutureEvent())
                  result += "]"
                  return result, firstItem
              
    def getColor(self):
        #COLOR BASED ON CLASS
        choose = {'Driver':'black',
                  'Business': 'yellow',
                  'Map': 'gold2x' 
                  }
        aClass = self.__class__.__name__
        if aClass in choose:
            return choose[aClass]

        #SELECT BASED On (CLASS, FUTURE EVENTS)
        hasFutureEvent = self.hasFutureEvent()
        choose = {('Politician',True):"orange",
                  ('Organization',True):"red",
                  ('Politician',False):"blue",
                  ('Organization',False):"red",
                  ('Location',True):"bluered",
                  ('Location',False):"blue",
                  ('Company',True):"yellow2x",
                  ('Company',False):"yellow"                                    
                  }
        icon = choose[(aClass,bool(hasFutureEvent))]
        return icon
                        
class MarkerLocation(MapOrLocation, PageMixIn):
    def getMarkerLatLng (self):
           #OOPS AN ANCIENT TYPO
           if hasattr(self,'lattitude'):
               if  self.lattitude != 0:
                   self.latitude = self.lattitude
               #del self.lattitude

           if hasattr(self,'longintude'):
               if  self.longintude != 0:
                   self.longitude = self.longintude
               #del self.longintude
           return self.latitude, self.longitude

           
    def setMarkerLatLng(self, lat,lng):
        self.latitude = lat
        self.longitude = lng

#At least used by events. 
@implementer (ILocationLeaf)
class LocationLeaf (MarkerLocation):
    icon="ttwicons/Location.svg"
    def getCompanies(self):
        return self
    def getCompaniesRecursively(self,context,result):
        return result.append(self)
        
@implementer (ILocationContainer)
class LocationContainer (MarkerLocation):
    icon="ttwicons/Location.svg"    
    def getCompanies(self):
        result=[]
        return self.getCompaniesRecursively(result,showChildren=False)

    def getCompaniesRecursively(self,result, showChildren = None):
        values = self.values()
        for item in values:
            #FOR APPROVED ORGANIZATIONS
            #FOR POLITICIANS, DO IT FIRST
            if not ILocationOrMap.providedBy(item):
                continue

            if not item.webApproved:
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
    clientClass = 'Category'
    icon="ttwicons/Map.svg"
    
      
    # GET THE JSON FOR CHILD LOCATIONS
    def getLocationsJSON(self):
        firstItem=True
        result=""   
        begin= "var locations =["
        end="\n];"
        result, firstItem= self.getLocationsJSONCore(
                                firstItem,result)
        return begin + result + end


    def getLocationsJSONCore(self,firstItem,result):
        if self.showChildren == True:
             mapPoints = self.values()
        else:
             mapPoints = self.getCompanies()
             
        for item in mapPoints:
             if not ILocationOrMap.providedBy(item):
                   continue
               
             if not item.webApproved:
                    continue
                               
             lat, lng = item.getMarkerLatLng()  
             if ((lat == 0) or
                 lng == 0):
                 continue
             
             # IF LOCATION GET THE JSON
             if ( ILocationOrMap.providedBy(item)):
                result, firstItem= item.getOneMarker(firstItem,result)

        return result , firstItem

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
            if (ILocationOrMap.providedBy(item) and 
                item.webApproved):
                result.append(item)
        return result

#So the old maps had a center
#Which was also their Marker
@implementer (IMap)
class Map(MapBase,LocationContainer,PageMixIn):        
    pass
