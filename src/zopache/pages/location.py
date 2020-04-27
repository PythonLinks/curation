
from .interfaces import ILocation, ILocationBase,IMap
from zope.interface import implementer
from .geo import geoCache
from zopache.pages.cache import cache, PageMixIn, RecentMixIn
from zopache.business.interfaces import IMap, ICompanyOrOrganization
from zopache.pages.page import PageBase
from zopache.pages.interfaces import IPage , IRootPage

class LocationBase (PageBase):
    lattitude = 45.
    longintude = 0.
    webClass = 'Location'
    specialization = ''
    
    def postProcess(self, view = None):
          #geoCache.geoCode(self.context.address)
          pass

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
                  result +=  str(self.lattitude)  
                  result += ','    
                  result += str(self.longitude)
                  color = self.getColor()
                  result += ",'" + color + "']"
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
        choose = {('Politician',True):"blue2x",
                  ('Organization',True):"red2x",
                  ('Politician',False):"blue",
                  ('Organization',False):"red",
                  ('Location',True):"blue2x",
                  ('Location',False):"blue"                  
                  }
        icon = choose[(aClass,hasFutureEvent)]
        print (icon,self.title, hasFutureEvent, '<-')
        return icon
              
              
    def getCompanies(self):
        result=[]
        return self.getCompaniesRecursively(result)

    def getCompaniesRecursively(self,result):
        values = self.values()
        for item in values:
            if (ICompanyOrOrganization.providedBy(item) and
                item.webApproved):
                result.append(item)
                
            if (IMap.providedBy(item)):
                item.getCompaniesRecursively(result)

            if (ILocation.providedBy(item)):
                item.getCompaniesRecursively(result)                

        return result
    
@implementer (ILocation)
class Location (LocationBase, PageMixIn):
    icon="ttwicons/Location.svg"

import googlemaps
class MapBase(LocationBase):
    zoomLevel=5.
    mapHeight=0.
    mapWidth=0.
    webClass = 'GoogleMap'
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
        for item in self.values():
             if not ILocationBase.providedBy(item):
                   continue
               
             if not item.webApproved:
                    continue
               
             elif ((item.lattitude == 0) and
                 item.longitude == 0):
                 continue
             
             # IF LOCATION GET THE JSON
             elif ( ILocationBase.providedBy(item)):
                result, firstItem= item.getOneMarker(firstItem,result)

            #IF IF IS A MAP SHOW IT
            #OR SHOW A SINGLETON CHILD
             elif ( IMap.providedBy (item)): 
                  #location=item.onlyOneLocationIn()
                  #if (location!=None):
                  #   item = location
                  result, firstItem= item.getOneMarker(  
                            firstItem,result)

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
            if (ILocation.providedBy(item) and 
                item.webApproved):
                result.append(item)
        return result

    
@implementer (IMap)
class Map(MapBase,PageMixIn):        
    pass
