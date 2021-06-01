import crom
from dolmen.container import IBTreeContainer
from zopache.python.interfaces import IFile, IDirectory,IPythonScript
from zopache.zmi.interfaces import IURLSegment
from zopache.pages.interfaces import INotebook
from zopache.python.iskulpt import ISkulptSolution

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

from zopache.python.iskulpt import ISkulptAssignment, ISkulptSolution
@crom.adapter
@crom.sources(ISkulptAssignment)
@crom.target(IURLSegment)
class ISkulptAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'index'


@crom.adapter
@crom.sources(ISkulptSolution)
@crom.target(IURLSegment)
class SolutinAdaptor(object):
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

from zopache.python.interfaces import IPyodide    
@crom.adapter
@crom.sources(IPyodide)
@crom.target(IURLSegment)
class IPythonScriptAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'aceedit'        


