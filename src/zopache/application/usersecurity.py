#Copyright Christopher Lozinski
#Basically this file imposes security based on a branch of the tree.

from cromlech.security import Unauthorized
from cromlech.security.principal import UnauthenticatedPrincipal 
from cromlech.security import unauthenticated_principal as anonymous


class UserSecurity(object):
    def __init__(self,view):
        self.view = view
            
    def check(self):
        principal = self.view.request.principal
        if principal == anonymous:
           raise Unauthorized()
        if 'Manage' in principal.permissions:
            return True
        if self.view.context is principal:
            return True 
        if self.view.context.__parent__ is principal:
            return True       
        raise Unauthorized()        

