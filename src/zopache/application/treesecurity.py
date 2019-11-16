#Copyright Christopher Lozinski
#Basically this file imposes security based on a branch of the tree.

from cromlech.security import Unauthorized
from zopache.core.relatives import Parents
from cromlech.security.principal import UnauthenticatedPrincipal 

class TreeSecurity(Parents):
    def __init__(self,view):
        self.view = view
        
    def isLocalEditor(self,name):
        context = self.view.context
        for category in self.reversedParentsUpToZodbRoot(context):
            if hasattr(category,'editors'):
                if name in category.editors:
                   return True
        return False
    
    def hasEditorPermission(self):
         view = self.view
         principal = view.request.principal
         if principal.__class__  == UnauthenticatedPrincipal:
             return False
         principalName = principal.__name__
         return self.isLocalEditor(principalName)

    def check(self):
        if not (self.hasEditorPermission()):
                raise Unauthorized()        

