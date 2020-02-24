import googlemaps
from zope.schema import Text
from zope.schema import ValidationError


class GeoCode(object):
    postAmble = """ When you submit the form, please be patient, 
            the server has to contact Google GeoCoding to 
            convert the address into a lattitude and longitude.  That   
            takes a few seconds. """
    
    def getLatLong(self,data):   
        gmaps = googlemaps.Client(key='AIzaSyDcxk6rq4CA3dFsUzIwYde5K3fIfCMq8y4')
        # Geocoding an address
        geocode_result = gmaps.geocode(data)
        result=geocode_result[0][u'geometry'] [u'location']
        lat = float(result [u'lat'])
        lng = float(result [u'lng'])
        return lat, lng

    def postAddProcess(self,view=None):
        GeoCode.postProcess(self,view=view)
        
    def postProcess (self,view=None):
         lat, lng = self.getLatLong(self.address)
         self.lattitude=lat 
         self.longitude=lng     

class GeoCodingError(ValidationError):
        __doc__ ="""That address is invalid."""
        
class Address (Text,GeoCode):
     def _validate (self,data):
         Text._validate(self,data)
         try:
             self.getLatLong(data)
         except:
             raise GeoCodingError("Illegal Address")

