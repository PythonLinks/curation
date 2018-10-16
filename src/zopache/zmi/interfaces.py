import crom
from zope.interface import Interface
from dolmen.container import IBTreeContainer

class IURLSegment(Interface):
    pass

"""
@crom.adapter
@crom.sources(Interface)
@crom.target(IURLSegment)
class IEditAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'edit'
"""

    
@crom.adapter
@crom.sources(IBTreeContainer)
@crom.target(IURLSegment)
class IManageAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'manage'    



class IObjectCutter(Interface):
     pass

class IObjectCopier(Interface):
     pass

class IObjectDeleter(Interface):
     pass

class IObjectRenamer(Interface):
     pass

class IObjectRetitler(Interface):
     pass 

class IObjectPaster(Interface):
     pass
