from zopache.business.interfaces import IMap, ICompany
from zope.interface import implementer
from zopache.pages.location import MapBase
from zopache.categories.category import Category

@implementer (IMap)
class Map  (Category,MapBase):
    webClass = "GoogleMap"
    hidden = False
    interface = IMap
    
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
        
