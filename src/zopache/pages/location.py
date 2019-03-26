from .interfaces import ILocation, IMap
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

  
    #JUST ADD ONE MARKER TO THE LIST                        
    def getOneMarker(self, firstItem, result):
                  if not hasattr(self, 'longitude'):
                      return result,firstItem
                  if not firstItem:
                     result +=','
                  firstItem=False      
                  result+='\n'
                  result += '['
                  result +='\'' +  self.__name__ + '\''
                  result += ','
                  result +='\'' +  self.title + '\''
                  result += ','                      
                  result +=  str(self.lattitude)  
                  result += u','    
                  result += str(self.longitude)
                  result += ']'
                  return result, firstItem

@implementer (ILocation)
class Location (LocationBase, RecentMixIn):
    icon="ttwicons/Location.svg"

              
import googlemaps
@implementer (IMap)
class Map(LocationBase,PageMixIn):
    zoomLevel=5.
    mapHeight=0.
    mapWidth=0.
    webClass = 'GoogleMap'
    icon="ttwicons/Map.svg"
      
    # GET THE JSON FOR CHILD LOCATIONS
    def getLocationsJSON(self):
        firstItem=True
        result=''             
        begin= 'var locations =['
        end='\n];'
        result, firstItem= self.getLocationsRecursively(
                                firstItem,result)
        return begin + result + end


    def getLocationsRecursively(self,firstItem,result):

        for item in self.values():
             if not ILocation.providedBy(item):
                   continue

             # IF LOCATION GET THE JSON
             if ( item.webClass=='Location'):
                result, firstItem= item.getOneMarker(firstItem,result)

            #IF IF IS A MAP SHOW IT
            #OR SHOW A SINGLETON CHILD
             if ( item.webClass=='Map'): 
                  location=item.onlyOneLocationIn()
                  if (location!=None):
                     item = location
                  result, firstItem= item.getOneMarker(  
                            firstItem,result)

        return result , firstItem


    #ITERATE THROUGH THE CHILDREN
    # IF ONLY ONE COMPANY RETURN IT, ELSE RETURN NONE
    def onlyOneLocatinIn(self):
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
    
        
