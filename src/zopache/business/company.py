from zope.interface import implementer

from cromlech.security import Unauthorized

from zopache.pages.location import LocationBase
from zopache.business.interfaces import (ICompany, IMap,
                               IOrganization, ICompanyBase)
from zopache.pages.page import Page
from zopache.business.geocoding import GeoCodeObject
from zopache.business.subscribe import Member

class Base (GeoCodeObject,LocationBase,Member):
    hidden = False
    longitude = 0.
    lattitude = 0.
    def __init__(self):
        LocationBase.__init__(self)
        Member.__init__(self)
        GeoCodeObject.__init__(self)

    def getTitle(self):
         if self.hidden:
            return "Hidden"
         return self.title

    def getSpecialization(self):
        if hasattr(self,'specialization') and self.specialization != '':
           return self.specialization
        return self.description [0:20]
    
    def canView(self,view):
         if (self.hidden and
             (not view.isAuthenticated())):
             raise Unauthorized 
    """                        
    def getCompanies(self):
        result=[]
        return self.getCompaniesRecursively(result)

    def getCompaniesRecursively(self,result):
        values = self.values()
        for item in values:
            if (ICompanyBase.providedBy(item) and
                item.webApproved):
                result.append(item)
            elif (IMap.providedBy(item)):
                item.getCompaniesRecursively(result)
        return result
    """
    
    def postProcess(self,view=None):
        Page.postProcess(self, view = view)
        GeoCodeObject.postProcess(self,view = view)
        
    def postAddProcess(self,view=None):
        self.webApproved = False
        self.hidden = False
        GeoCodeObject.postAddProcess(self,view=view)
        Page.postAddProcess(self, view = view)
        
        #self.editors=[view.request.principal.__name__]
        
@implementer (ICompany)
class Company  (Base):
    webClass = "Company"
    clientClass = "category"

@implementer (IOrganization)
class Organization  (Base):        
    webClass = "Organization"
    clientClass = "Category"

