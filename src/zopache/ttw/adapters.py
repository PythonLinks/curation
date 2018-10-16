import crom
from zopache.zmi.interfaces import IURLSegment
from .interfaces import IAceHTML, IHTML, IHTMLContainer
from zopache.ttw.css import ICSS
#from .json import IJSON
from .javascript import IJavascriptFolder, IJavascript
from .interfaces import IHTMLClass
from .python import IPython

@crom.adapter
@crom.sources(IHTMLContainer)
@crom.target(IURLSegment)
class IHTMLContainerAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'manage'


@crom.adapter
@crom.sources(IAceHTML)
@crom.target(IURLSegment)
class IAceHTMLAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'aceedit'

@crom.adapter
@crom.sources(ICSS)
@crom.target(IURLSegment)
class ICSSAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'aceedit'

    
@crom.adapter
@crom.sources(IJavascript)
@crom.target(IURLSegment)
class IAceJavascriptAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'aceedit'        

"""
@crom.adapter
@crom.sources(IJSON)
@crom.target(IURLSegment)
class ICSSAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'aceedit'    
"""

@crom.adapter
@crom.sources(IJavascriptFolder)
@crom.target(IURLSegment)
class IJavascriptFolderAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'search'    

@crom.adapter
@crom.sources(IPython)    
@crom.target(IURLSegment)
class IPythonAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'aceedit'    



@crom.adapter
@crom.sources(IHTMLClass)
@crom.target(IURLSegment)
class ICkHTMLAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'ckedit'

"""
NOt WOrking.
Not my priority today. 
from .python import IPython    
@crom.adapter
@crom.sources(IPython)
@crom.target(IURLSegment)
class ICkEditAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'ckedit'            
"""




    
