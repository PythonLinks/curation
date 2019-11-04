
from .interfaces import ILocation, ILocationBase,IMap
from zopache.pages.page import PageBase
from zopache.pages.interfaces import IPage , IRootPage
from zope.interface import implementer
from .geo import geoCache
from zopache.pages.cache import cache, PageMixIn, RecentMixIn


class LocationBase (PageBase):
    lattitude = 45.
    longintude = 0.
    webClass = 'Location'

    def postProcess(self):
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
                  result += ',"red"]'
                  return result, firstItem
              

@implementer (ILocation)
class Location (LocationBase, RecentMixIn):
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
        result, firstItem= self.getLocationsRecursively(
                                firstItem,result)
        return begin + result + end


    def getLocationsRecursively(self,firstItem,result):
        for item in self.values():
             if not ILocationBase.providedBy(item):
                   continue
               
             if ((item.lattitude == 0) and
                 item.longitude == 0):
                 continue
             
             # IF LOCATION GET THE JSON
             if ( ILocationBase.providedBy(item)):
                result, firstItem= item.getOneMarker(firstItem,result)

            #IF IF IS A MAP SHOW IT
            #OR SHOW A SINGLETON CHILD
             if ( IMap.providedBy (item)): 
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
    
    """
    #NOT USED, BUT POTENTIALLY USEFUL
    def getLocations(self):
        values=self.values()
        result=[]
        for item in values:
            if (ILocation.providedBy(item) and 
                item.webApproved):
                result.append(item)
        return result
     """
    
@implementer (IMap)
class Map(MapBase,PageMixIn):        
    pass
