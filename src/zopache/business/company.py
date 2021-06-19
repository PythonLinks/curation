from zope.interface import implementer

from cromlech.security import Unauthorized
from zopache.pages.location import LocationContainer
from zopache.business.interfaces import IFollow
from zopache.business.interfaces import (ICompany, IMap,
                                         IOrganization,
                                         IOnlineOrganization,
                                         ICompanyBase,
                                         IMapOrganization)
from zopache.business.ipolitician import IPolitician
from zopache.pages.location import LocationLeaf
from zopache.pages.page import Page
from zopache.pages.interfaces import IPage
from zopache.business.geocoding import GeoCodeObject, GeoBase
from zopache.business.imaginarypage import ImaginaryPage
from zopache.business.subscribe import HasMembers
from zopache.business.map import Map
from zopache.pages.location import MapBase

class Base(Page):    
    hidden = False
    eventsPageURL = ""
    hasScheduledEvents = False  
    email = ''
    
    def __init__(self):
        Page.__init__(self)
        HasMembers.__init__(self)
        
    def getSpecialization(self):
        if hasattr(self,'specialization') and self.specialization != '':
           return self.specialization
        return self.description [0:20]


    
@implementer (ICompany)
class Company  (GeoBase,LocationContainer):
    webClass = "Company"
    clientClass = "category"

@implementer (IOnlineOrganization)
class OnlineOrganization  (Base,HasMembers):        
    webClass = "Organization"
    clientClass = "Category"
    webApproved = True
    def getCompaniesRecursively(self,result,showChildren = False):
        return [self]
    
from zopache.business.region import RegionBase
@implementer (IOrganization)
class Organization  (
                     GeoBase,
                     HasMembers,
                     LocationLeaf):
    
    interface = IOrganization
    webClass = "Organization"
    clientClass = "Category"
    webApproved = True
    donationsPageURL = ""
    youTubeChanneURL = ""
    ballotStatus = ""
    focus = ""
    twitterId = ""
    facebookId = ""
    facebookGroup = ""
    remoteURL = ""
    def getOneMarkerCore(self):
        focus = getattr(self,'focus',"")
        focus = focus [:4]
        return  ',"' + focus + '"'
    
#SO maps have Lattitude and Longitude.
#Companies now use getMarketLngLtd
from zopache.business.interfaces import IMapOrganization, IEndorsingOrganization
@implementer (IMapOrganization)
class MapOrganization(ImaginaryPage,
                      GeoBase,
                      MapBase,
                      HasMembers,
                      Page,
                      RegionBase):

    interface = IMapOrganization
    webClass = 'SmallParty'
    #LocationBase inherits from Page
    def __init__(self):
        Map.__init__(self)
        Organization.__init__(self)
        
    def getDescriptionForDomain(self,view):
        domain = view.getDomain()
        #HTML objects do not have a description, only a title and source
        if domain in self:
            item = self [domain]
            if hasattr(item,'description'):
                return item.description
            else:
                return item.source        
        else:
            return self.description
        
    def childCategories(self):
        result =[]
        for item in self.values():
            if IPolitician.providedBy(item):
                continue
            
            if IOrganization.providedBy(item):
                continue
            
            if (IPage.providedBy (item) and item.webApproved):
               result.append (item)
               
        return result
    
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
    

