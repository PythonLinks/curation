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
    
from zopache.core.getroot import getSiteRoot
class Base(object):

    def setLatLong(self):
        lat,lng = self.getLatLong (self.address)        
        self.setMarkerLatLng(lat,lng)

    def getLatLong(self,data):
        #key='AIzaSyDcxk6rq4CA3dFsUzIwYde5K3fIfCMq8y4')
        key =''
        siteRoot = getSiteRoot(self)
        if hasattr(siteRoot,'googleClientId'):
           if siteRoot.googleClientId:
              key = siteRoot.googleClientId 
        gmaps = googlemaps.Client()
        # Geocoding an address
        geocode_result = gmaps.geocode(data)
        result=geocode_result[0][u'geometry'] [u'location']
        lat = float(result [u'lat'])
        lng = float(result [u'lng'])
        return lat, lng

    
class GeoCodeObject(Base):
    address = ''
    def postProcess(self,view=None):
        Page.postProcess(self, view = view)
        if self.address:
            self.setLatLong()        
        
    def postAddProcess(self,view=None):
        self.hidden = False
        Page.postAddProcess(self, view = view)
        #Page calls post process, so lat lng  is not needed. 
        #self.editors=[view.request.principal.__name__]    

class GeoCodingError(ValidationError):
        __doc__ ="""That address is invalid."""
        
class Address (Text,GeoCodeObject):
     def _validate (self,data):
         Text._validate(self,data)
         try:
             self.getLatLong(data)
         except:
             raise GeoCodingError("Illegal Address")

