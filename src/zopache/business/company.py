from zope.interface import implementer

from cromlech.security import Unauthorized

from zopache.pages.location import LocationBase
from zopache.business.interfaces import (ICompany, IMap,
                                         IOrganization,
                                         IOnlineOrganization,
                                         ICompanyBase)
from zopache.pages.page import Page
from zopache.business.geocoding import GeoCodeObject
from zopache.business.subscribe import Member
from zopache.business.geocoding import GeoCodeObject

class VeryBase (Member):
    hidden = False

    def getTitle(self):
         if self.hidden:
            return "Hidden"
         return self.title

    def getSpecialization(self):
        if hasattr(self,'specialization') and self.specialization != '':
           return self.specialization
        return self.description [0:20]

class Base(VeryBase,Page):
    def __init__(self):
        Member.__init__(self)
        Page.__init__(self)    

#GeoBase inherits  Page from Location
class GeoBase(GeoCodeObject,Base,LocationBase):
    longitude = 0.
    lattitude = 0.
    #LocationBase inherits from Page
    def __init__(self):
        LocationBase.__init__(self)
        Member.__init__(self)
        GeoCodeObject.__init__(self)
        
    def canView(self,view):
         if (self.hidden and
             (not view.isAuthenticated())):
             raise Unauthorized 
    
@implementer (ICompany)
class Company  (GeoBase):
    webClass = "Company"
    clientClass = "category"

@implementer (IOnlineOrganization)
class OnlineOrganization  (Base):        
    webClass = "Organization"
    clientClass = "Category"
    webApproved = False

@implementer (IOrganization)
class Organization  (GeoBase):        
    webClass = "Organization"
    clientClass = "Category"
    webApproved = False    
