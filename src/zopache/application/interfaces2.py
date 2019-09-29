from zope.interface import implementer, Interface
from dolmen.container import IBTreeContainer

class IZodbRoot(Interface):
    pass

class IRootContainer(IZodbRoot, IBTreeContainer):
    pass
