import googlemaps
from zope.schema import Text
from zope.schema import ValidationError
from zopache.pages.page import Page

class GeoCodeForm(object):
    def update(self):
        pass
    
    postAmble = """ When you submit the form, please be patient, 
            the server has to contact Google GeoCoding to 
            convert the address into a lattitude and longitude.  That   
            takes a few seconds. """

class Base(object):

    def getLatLong(self,data):   
        gmaps = googlemaps.Client(key='AIzaSyDcxk6rq4CA3dFsUzIwYde5K3fIfCMq8y4')
        # Geocoding an address
        geocode_result = gmaps.geocode(data)
        result=geocode_result[0][u'geometry'] [u'location']
        lat = float(result [u'lat'])
        lng = float(result [u'lng'])
        return lat, lng

class GeoCodeObject(Base):
    def postProcess(self,view=None):
        Page.postProcess(self, view = view)
        GeoCodeObject.postProcess(self,view = view)
        
    def postAddProcess(self,view=None):
        self.webApproved = False
        self.hidden = False
        GeoCodeObject.postAddProcess(self,view=view)
        Page.postAddProcess(self, view = view)
        
        #self.editors=[view.request.principal.__name__]    

    def postAddProcess(self,view=None):
         self.postProcess(view = view)
         
    def postProcess (self,view=None):
         lat, lng = self.getLatLong(self.address)
         self.lattitude=lat 
         self.longitude=lng     

class GeoCodingError(ValidationError):
        __doc__ ="""That address is invalid."""
        
class Address (Text,GeoCodeObject):
     def _validate (self,data):
         Text._validate(self,data)
         try:
             self.getLatLong(data)
         except:
             raise GeoCodingError("Illegal Address")

