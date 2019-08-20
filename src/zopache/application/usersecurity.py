#Copyright Christopher Lozinski
#Basically this file imposes security based on a branch of the tree.

from cromlech.security import Unauthorized
from zopache.core.breadcrumbs import parents
from cromlech.security.principal import UnauthenticatedPrincipal 

class UserSecurity(object):
    def __init__(self,view):
        self.view = view
            
    def check(self):
        if 'Manage' in self.view.request.principal.permissions:
            return True
        if self.view.context is self.view.request.principal:
            return True 
        if self.view.context.__parent__ is self.view.request.principal:
            return True       
        raise Unauthorized()        

