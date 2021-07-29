from zopache.pages.address import Base
from cromlech.security import Unauthorized
from zopache.pages.location import LocationContainer

class GeoCodeForm(object):
    def update(self):
        pass
    
    postAmble = """ When you submit the form, please be patient, 
            the server has to contact Google GeoCoding to 
            convert the address into a lattitude and longitude.  That   
            takes a few seconds. """
    
class GeoCodeObject(Base):
    address = ''
    
    def postProcess(self,view=None):
        super().postProcess(view = view)
        if self.address:
            self.setLatLong()        
        
    def postAddProcess(self,view=None):
        self.hidden = False
        super().postAddProcess(view = view)
        self.postProcess(view=view)
        #Page calls post process, so lat lng  is not needed. 
        #self.editors=[view.request.principal.__name__]    
    

        
#GeoBase inherits  Page from Location
class GeoBase(GeoCodeObject):
    #LocationBase inherits from Page
    def __init__(self):
        LocationContainer.__init__(self)
        GeoCodeObject.__init__(self)
        
    def canView(self,view):
         if (self.hidden and
             (not view.isAuthenticated())):
             raise Unauthorized 
