from zope import schema
from zope.schema import ValidationError
import googlemaps    
class GeoCode(object):
   lastAddress = None
   lat = 0 
   long = 0
 

    # Geocoding an address    
   def geoCode(self,address):
        
        if address == self.lastAddress:
          return self.lat, self.long 
        self.lastAddress = address        
        gmaps = googlemaps.Client(
              key='YOUR KEY HERE')

        geocode_result = gmaps.geocode(self.address)
        result=geocode_result[0][u'geometry'] [u'location']
        self.lat=float(result [u'lat'])
        self. long=float(result [u'lng'])
        return self.lat, self.long

geoCache = GeoCode()    
class Address (schema.Text):
    def validate(self,value):
        try:
            geoCache.geocode(value)
        except:
            raise ValidationError('THat is not a good address')   
    
