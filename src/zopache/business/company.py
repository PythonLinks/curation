from .interfaces import ICompany, IMap
from zope.interface import implementer
from zopache.pages.location import LocationBase
from zopache.categories.category import Category
from cromlech.security import Unauthorized

@implementer (ICompany)
class Company  (Category,LocationBase):
    hidden = False
    webClass = "Company"
    longitude = 0.
    lattitude = 0.
    def getTitle(self):
         if self.hidden:
            return "Hidden"
         return self.title
    
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
        
        
