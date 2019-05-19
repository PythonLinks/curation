from .interfaces import ICompany
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
              
          
        
