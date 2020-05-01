import crom
from dolmen.container import IBTreeContainer
from zopache.python.interfaces import IFile, IDirectory,IPythonScript
from zopache.zmi.interfaces import IURLSegment
from zopache.pages.interfaces import INotebook

#FOR BTREES    
@crom.adapter
@crom.sources(IDirectory)
@crom.target(IURLSegment)
class IDirectoryAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'manage'

@crom.adapter
@crom.sources(IFile)
@crom.target(IURLSegment)
class IFileAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'index'

@crom.adapter
@crom.sources(IPythonScript)
@crom.target(IURLSegment)
class IPythonScriptAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'aceedit'    


