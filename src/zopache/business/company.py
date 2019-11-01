from .interfaces import ICompany, IMap, IOrganization
from zope.interface import implementer
from zopache.pages.location import LocationBase
from zopache.categories.category import Category
from cromlech.security import Unauthorized


class Base (Category,LocationBase):
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
            if (ICompany.providedBy(item) and
                item.webApproved):
                result.append(item)
            if (IMap.providedBy(item)):
                item.getCompaniesRecursively(result)
        return result

@implementer (ICompany)
class Company  (Base):
    webClass = "Company"
    clientClass = "category"

@implementer (IOrganization)
class Organization  (Base):        
    webClass = "Company"
    clientClass = "Category"

