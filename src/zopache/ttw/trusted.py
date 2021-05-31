from cromlech.security import unauthenticated_principal as anonymous

class Trusted (object):

    def setTrusted(self,view=None):            
            principal = view.request.principal
            if principal == anonymous:
               self.trusted = False
               return
       
            if 'Python' in view.request.principal.permissions:
               self.trusted = True
            else:
               self.trusted = False

