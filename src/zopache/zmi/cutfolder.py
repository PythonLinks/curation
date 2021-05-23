from dolmen.container import BTreeContainer
from cromlech.security.principal import UnauthenticatedPrincipal

class CutFolder (BTreeContainer):
    def getFromWebClass(self, name, marker=None):
        return marker
    
def cutFolder(view):
        principal = view.request.principal
        if principal.__class__  == UnauthenticatedPrincipal:
            return []
       
        if not 'cutFolder' in principal:
             principal ['cutFolder'] = CutFolder()
             
        return principal ['cutFolder']
