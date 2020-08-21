from zope.interface import implementer

from cromlech.security import Unauthorized
from zopache.pages.location import LocationContainer

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
    email = ''    
    def __init__(self):
        Member.__init__(self)
        Page.__init__(self)    

#GeoBase inherits  Page from Location
class GeoBase(GeoCodeObject,Base):
    longitude = 0.
    lattitude = 0.
        
    #LocationBase inherits from Page
    def __init__(self):
        LocationContainer.__init__(self)
        Member.__init__(self)
        GeoCodeObject.__init__(self)
        
    def canView(self,view):
         if (self.hidden and
             (not view.isAuthenticated())):
             raise Unauthorized 
    
@implementer (ICompany)
class Company  (GeoBase,LocationContainer):
    webClass = "Company"
    clientClass = "category"

@implementer (IOnlineOrganization)
class OnlineOrganization  (Base):        
    webClass = "Organization"
    clientClass = "Category"
    webApproved = False

from zopache.business.region import Region    
@implementer (IOrganization)
class Organization  (GeoBase,LocationContainer,Region):
    interface = IOrganization
    webClass = "Organization"
    clientClass = "Category"
    webApproved = False
    #USED SO IT LOOKS LIKE A POLITICIAN
    #TO THE TEMPLATES
    def proxyValues():
        return self.values()



    
#SO maps have Lattitude and Longitude.
#Companies now use getMarketLngLtd
from zopache.business.interfaces import IMapOrganization, IEndorsingOrganization
from zopache.business.map import Map
from zopache.business.subscribe import Member        
from zopache.pages.location import MapBase

@implementer (IMapOrganization)
class MapOrganization(GeoBase,
                      MapBase,
                      Member,
                      Page,
                      Region):

    interface = IMapOrganization
    webClass = 'SmallParty'
    #LocationBase inherits from Page
    def __init__(self):
        Map.__init__(self)
        Organization.__init__(self)

from zopache.core.getroot import getSiteRoot
from zopache.business.interfaces import IEndorsingOrganization
@implementer(IEndorsingOrganization)    
class EndorsingOrganization(MapBase,Organization):
    interface = IEndorsingOrganization
    webClass = "EndorsingOrganization"
    _endorsedPoliticians = []

    @property
    def endorsedPoliticians(self):
        siteRoot = getSiteRoot(self)
        for item in self._endorsedPoliticians:
            if not item in siteRoot:
                continue
            yield siteRoot[item]
    
    def getCompanies(self):
        return self.endorsedPoliticians
    

