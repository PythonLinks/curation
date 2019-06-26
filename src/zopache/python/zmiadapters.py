import crom
from dolmen.container import IBTreeContainer
from zopache.python.interfaces import IFile, IDirectory
from zopache.zmi.interfaces import IURLSegment


#FOR BTREES    
@crom.adapter
@crom.sources(IDirectory)
@crom.target(IURLSegment)
class IManageAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'manage'

@crom.adapter
@crom.sources(IFile)
@crom.target(IURLSegment)
class IPythonAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'index'
