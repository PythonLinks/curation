from zopache.core.getroot import getSiteRoot
from zope.schema import Text
import googlemaps
from zope.schema import ValidationError

class GeoCodingError(ValidationError):
        __doc__ ="""That address is invalid."""

class Address (Text):
    def setLatLong(self):
        lat,lng = self.getLatLong (self.address)        
        self.setMarkerLatLng(lat,lng)

    def getLatLong(self,data):
        key='AIzaSyDcxk6rq4CA3dFsUzIwYde5K3fIfCMq8y4' 
        #siteRoot = getSiteRoot(self)
        #if hasattr(siteRoot,'googleClientId'):
        #   if siteRoot.googleClientId:
        #      key = siteRoot.googleClientId 
        gmaps = googlemaps.Client(key)
        # Geocoding an address
        geocode_result = gmaps.geocode(data)
        result=geocode_result[0][u'geometry'] [u'location']
        lat = float(result [u'lat'])
        lng = float(result [u'lng'])
        return lat, lng
            
    def _validate (self,data):
         Text._validate(self,data)
         try:
             self.getLatLong(data)
         except:
             raise GeoCodingError("Illegal Address")
        
