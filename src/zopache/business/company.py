from zope.interface import implementer

from cromlech.security import Unauthorized

from zopache.pages.location import LocationBase
from zopache.categories.category import Category
from zopache.business.interfaces import (ICompany, IMap,
                               IOrganization, ICompanyBase)
from zopache.business.geocoding import GeoCode
from zopache.pages.page import Page
from zopache.business.geocoding import Address


class Base (GeoCode,LocationBase):
    hidden = False
    longitude = 0.
    lattitude = 0.
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

    def postAddProcess(self):
        self.new.webApproved = False
        self.new.hidden = True
        Address.postAddProcess(self.new)
        Page.postAddProcess(self.new)
    
@implementer (ICompany)
class Company  (Base):
    webClass = "Company"
    clientClass = "category"

@implementer (IOrganization)
class Organization  (Base):        
    webClass = "Company"
    clientClass = "Category"

