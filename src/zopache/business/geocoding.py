import googlemaps
from zope.schema import Text
from zope.schema import ValidationError
from zopache.ttw.html import UserCkEditForm

class GeoCode(object):
    postAmble = """ When you submit the form, please be patient, 
            the server has to contact Google GeoCoding to 
            convert the address into a lattitude and longitude"""
    
    def getLatLong(self,data):   
        gmaps = googlemaps.Client(key='AIzaSyDcxk6rq4CA3dFsUzIwYde5K3fIfCMq8y4')
        # Geocoding an address
        geocode_result = gmaps.geocode(self.context.address)
        result=geocode_result[0][u'geometry'] [u'location']
        lat = float(result [u'lat'])
        lng = float(result [u'lng'])
        return lat, lng

    def postAddProcess(self,view):
        self.postProcess(view)
        
    def postProcess (self,view):
         lat, lng = self.getLatLong()
         self.context.lattitude=lat 
         self.context.longitude=lng     

class GeoCodingError(ValidationError):
        __doc__ ="""That address is invalid."""
        
class Address (Text,GeoCode):
     def _validate (self,data):
         import pdb; pdb.set_trace()
         Text._validate(self,data)
         try:
             self.getLatLong(data)
         except:
             raise GeoCodingError("Illegal Address")

