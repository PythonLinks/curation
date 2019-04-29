from .interfaces import ICompany
from zope.interface import implementer
from zopache.pages.location import LocationBase
from zopache.categories.category import Category
from cromlech.security import Unauthorized

@implementer (ICompany)
class Company  (Category,LocationBase):
     webClass = "Company"

     def canView(self,view):
         parent = self.__parent__
         if (hasattr(parent,"hidden") and
             (parent.hidden == True) and
             (not view.isAuthenticated())):
             raise Unauthorized 
              
          
        
