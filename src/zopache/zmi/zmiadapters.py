import crom
from dolmen.container import IBTreeContainer
from zopache.ttw.interfaces import IJSON
from zopache.python.interfaces import IPython
from zopache.ttw.interfaces import IInternalPrincipal
from zopache.zmi.interfaces import IURLSegment


"""
# THIS ONE IS FOR EDITING ANY INTERFACE
@crom.adapter
@crom.sources(Interface)
@crom.target(IURLSegment)
class IEditAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'edit'
"""

#FOR BTREES    
@crom.adapter
@crom.sources(IBTreeContainer)
@crom.target(IURLSegment)
class IManageAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'manage'

    

#FOR JSON
@crom.adapter
@crom.sources(IJSON)
@crom.target(IURLSegment)
class IJSONAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'aceedit'

@crom.adapter
@crom.sources(IPython)
@crom.target(IURLSegment)
class IPythonAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'aceedit'

"""
THERE IS ANOTHER ONE FOR return 'permissions'
@crom.adapter
@crom.sources(IInternalPrincipal)
@crom.target(IURLSegment)
class IPrincipalAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'edit'            
"""    

# FOR A PRINCIPAL
from zopache.ttw.interfaces import IInternalPrincipal
@crom.adapter
@crom.sources(IInternalPrincipal)
@crom.target(IURLSegment)
class IPrincipalAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'manage'    
    
