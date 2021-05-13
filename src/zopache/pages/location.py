from zope.interface import implementer
from zopache.pages.geo import geoCache
from zopache.pages.cache import cache, PageMixIn, RecentMixIn
from zopache.pages.page import PageBase
from zopache.pages.interfaces  import (IPage,
                                       IRootPage,
                                       ILocationContainer,
                                       ILocationOrMap,
                                       ILocationLeaf,
                                       ILocation,
                                       IMap
                                       )

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
                  result += ","                   
                  result += str(lng)
                  aClass = self.__class__.__name__[0]
                  result += self.getArg(aClass)
                  hasFutureEvent =  str(self.hasFutureEvent())
                  result += self.getArg(hasFutureEvent)
                  if self.__class__.__name__ in [
                          "Organization","MapOrganization"]:
                      focus = getattr(self,'focus',"")
                      focus = focus [:4]
                      result += ',"' + focus + '"'
                      
                  if self.__class__.__name__ == "Politician":
                     result += self.getArg(str(hasattr(
                                        self,'candidateInfo'))[0])
                     result += self.getArg(str(hasattr(
                                        self,'electedOfficial'))[0])
                     result += self.getArg(
                          str(hasattr(self,'partyOfficer'))[0])
                     result += self.getArg(
                          str(hasattr(self,'history'))[0])                     
                     outcome = self.getCandidateInfo("result")
                     if len(outcome) > 0:
                         outcome = outcome [0]
                     result += ',"' + outcome +' "'
                     
                  result += ',"' + self.remoteURL  + '"'                  
                  result += "]"
                  return result, firstItem
              
    def isElectedOfficial(self):
        if hasattr(self,'electedOfficial'):
           return True
        if self.getCandidateInfo("result") =="Won":
           return True
        return False                                   

    def getArg(self,aString,comma = True):
          result = ""
          if comma:
              result += ","
          result += '"'
          result += aString
          result += '"'
          return result
      
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
        choose = {
                  ('Politician',True):"orange",
                  ('Politician',False):"blue",
                  ('City',True):"orange",
                  ('City',False):"blue",            
                  ('MapOrganization',False):"red",                  
                  ('MapOrganization',True):"orange",                  
                  ('Organization',False):"red",
                  ('Organization',True):"orange",
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
    
    def getCompaniesRecursively(self,result,showChildren = False):
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
    clientClass = 'Category'
    icon="ttwicons/Map.svg"
    
      
    # GET THE JSON FOR CHILD LOCATIONS
    def getLocationsJSON(self, view = None):
        firstItem=True
        result=""   
        begin= "["
        end="\n]"
        result, firstItem= self.getLocationsJSONCore(
                                firstItem,result,view)
        return begin + result + end

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
                mapPoints.append(item)
        return mapPoints
     
    def getLocationsJSONCore(self,firstItem,result,view):
        for item in self.mapPoints():
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
