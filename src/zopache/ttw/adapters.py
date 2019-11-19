import crom
from zopache.zmi.interfaces import IURLSegment
from .interfaces import IAceHTML, IHTML, IHTMLContainer
from zopache.ttw.css import ICSS
#from .json import IJSON
from .javascript import IJavascriptFolder, IJavascript
from .pug import IPug
from .interfaces import IHTMLClass
#from .python import IPython
from zopache.ttw.interfaces import IFile, IImage

@crom.adapter
@crom.sources(IHTMLContainer)
@crom.target(IURLSegment)
class IHTMLContainerAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'manage'


from zopache.ttw.interfaces import IMailHost    
@crom.adapter
@crom.sources(IMailHost)
@crom.target(IURLSegment)
class IMailHostAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'edit'    

from .coffeescript import ICoffeeScript    
@crom.adapter
@crom.sources(ICoffeeScript)
@crom.target(IURLSegment)
class ICoffeeScriptAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'aceedit'    

@crom.adapter
@crom.sources(IFile)
@crom.target(IURLSegment)
class IFileAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'index'

@crom.adapter
@crom.sources(IImage)
@crom.target(IURLSegment)
class ImageAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'index'        


@crom.adapter
@crom.sources(IAceHTML)
@crom.target(IURLSegment)
class IAceHTMLAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'aceedit'


#FOR Pug
@crom.adapter
@crom.sources(IPug)
@crom.target(IURLSegment)
class IPugAdaptor(object):
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


"""
@crom.adapter
@crom.sources(IPython)    
@crom.target(IURLSegment)
class IPythonAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'aceedit'    
"""


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




    
