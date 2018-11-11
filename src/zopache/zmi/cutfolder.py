from dolmen.container import BTreeContainer

class CutFolder (BTreeContainer):
    pass

def cutFolder(view):
        principal = view.request.principal
        if not 'cutFolder' in principal:
             principal ['cutFolder'] = CutFolder()
             
        return principal ['cutFolder']
