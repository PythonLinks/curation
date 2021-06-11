from jsmin import jsmin
from zopache.ttw import tal_template
from html import escape
from zope import interface
from zope import schema
from zope.schema.interfaces import IField
from zope.interface import Interface
from zopache.ttw.interfaces import ITestSource as ISource
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.crud.forms import EditDemoForm
from zopache.core.viewdecorators import *
from dolmen.container import IBTreeContainer,BTreeContainer
from zopache.core import Leaf
from zopache.ttw.acescripts import AceScripts
from zopache.core.page  import  Page
from .interfaces import ITestURL
from cromlech.webob.response import Response
from .interfaces import IJavascript,IJavascriptIndex
from zopache.core.relatives import Parents
from zopache.core.interfaces import ITreeSecurity
from zopache.ttw.interfaces import IJavascriptFolder,ISearchable

@title("Add JavascriptFolder")
class SourceBase(object):
    def getJavascriptObjects(self):
         return [self]

    def getLines(self):
         result=self.getSource()
         result=escape(result)
         result=result.replace(' ','&nbsp')
         return result.split("\n")
    
    def getTitle(self):
        return self.__name__

    def getSource(self):
        return self.source
    
class JavascriptBase(SourceBase):
    
    def getJavascript(self):
        return self.source
    
    def postProcess(self,view=None):    
        self.createJavascriptCaches()

    #THIS CAN BE REMOVED    
    def postEditProcess(self,view=None):    
        self.postProcess(view=view)
        
    def postAddProcess(self,view=None):    
        self.postProcess(view=view)

    def createJavascriptCaches(self):
        parentJavascriptFolders=Parents(self
                         ).parentsWhichImplement(IJavascriptFolder)
        for folder in parentJavascriptFolders:
             folder.sourceCache= folder.getCompressedCode()

    def getCompressedCode(self):
        return jsmin(self.getJavascript())

    def __call__(self,view,**args):
            return self.getJavascript()       
    
@implementer(IJavascript)      
class Javascript(JavascriptBase,Leaf):
    icon="ttwicons/Javascript.svg"    
    source =u''
    title=u''
    className='Javascript'




                
class JavascriptFolderBase (BTreeContainer):   
    source =u''
    sourceCache=u''
    def cacheSource(self):
        self.sourceCache=self.getJavascript()
        
    def __delitem__(self,key):
        BTreeContainer.__delitem__(self,key)
        item = self[key]
        self.createJavascriptCaches()
        
    def __setitem__(self,  key,item):
        BTreeContainer.__setitem__(self,key,item)
        self.createJavascriptCaches()        

    def getJavascript(self):
        result = self.source or ' '
        for item in self.values():
            if hasattr(item, 'getJavascript'):
                result +=item.getJavascript()
                result += '\n'
        return result

    def getSource(self):
        result = self.source or ' '
        for item in self.values():
            result +=item.getSource()
            result += '\n'
        return result

    def getJavascriptObjects(self):
         result=[]
         for item in self.values():
             if IJavascript.providedBy(item):
                result+= item.getJavascriptObjects()
         return result

    def flatten(self,view):
         result=[]
         count=1
         class Record(object):
              pass
         objects=self.getJavascriptObjects()
         for anObject in objects:
             #JUST A LINE FOR THE FILE
             lines=anObject.getLines()
             o=Record()
             o.line=view.href(view.url(anObject)+'/aceedit', anObject.__name__)
             o.line="<h3>"+o.line+"</h3>"
             o.count=''
             result.append(o)

             for line in anObject.getLines():
                 o=Record()
                 o.line=line.replace(' ','&nbsp;')
                 o.count=view.href(view.url(anObject)+'/aceedit', str(count))
                 count=count+1
                 result.append(o)

         return result

@implementer(IJavascriptFolder)
class JavascriptFolder(JavascriptFolderBase,Javascript):
    className='Javascript Folder'
    icon="ttwicons/JavascriptFolder.svg"    

    
@form_component
@name('addJavascript')
@context(IBTreeContainer)
@target(IView)
@title("Add Javascript")
#@permissions('Manage')
@implementer(ITreeSecurity)
class AddJavascript(AceAddForm):
    aceMode = "javascript"
    subTitle='Add a Javascript Object'
    interface = IJavascript
    ignoreContent = True
    factory=Javascript
    
#    def postProcess(self,view=None):
#        self.new.postProcess(view=view)


    
@form_component
@name('addJavascriptFolder')
@context(IBTreeContainer)
@target(IView)
@title("Add JavascriptFolder")
#@permissions('Manage')
@implementer(ITreeSecurity)
class AddJavascriptFolder(AceAddForm):
    aceMode = "javascript"
    subTitle= 'Add a Javascript Folder'
    interface = IJavascriptFolder
    ignoreContent = True
    factory=JavascriptFolder    


        
def makeJavascriptResponse(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or u'')
        response.content_type=u'application/javascript' 
        return response

@view_component
@name('index')
@context(IJavascriptIndex)
class JavascriptIndex(Page):
    responseFactory = Response
    make_response = makeJavascriptResponse
        
    def render(self ):
            if IJavascriptFolder.providedBy(self.context):
                   return self.context.sourceCache
            else: 
                   return self.context.getJavascript()



from zopache.ttw.interfaces import IGrapeBase
@view_component
@name('index')
@context(IGrapeBase)
class GrapeIndex(Page):
    responseFactory = Response
    make_response = makeJavascriptResponse
        
    def render(self ):
        return self.context.javascript

class BaseJavascript(AceScripts):
    aceMode = "javascript"    
    subTitle='Ace Edit this  Javascript'
    label=''
    
#HERE WE HAVE THE ACE EDIT FORM               
@form_component
@context(IJavascript)
@target(IView)
@title("AceEdit")
@name("aceedit")
class AceEditJavascript(BaseJavascript,AceEditForm):
    pass

#AND HERE WE HAVE THE ACE DEMO FORM               
@form_component
@context(IJavascript)
@target(IView)
@name("acedemo")
class AceDemoJavascript(BaseJavascript,EditDemoForm):
      pass


        
@view_component
@name('search')
@title("Search")
@target(IView)
@context(IJavascriptFolder)
class Search(Page):
    subTitle=u'Search The Javascript'
    template = tal_template('javascriptFolder.pt')
    subTitle="Search Javascript Folder"
    className='Javacript Folder'

    def breadcrumbs(self):
        return self.breadcrumbsManage()


import crom
from zopache.zmi.interfaces import IURLSegment
@crom.adapter
@crom.sources(IJavascriptFolder)
@crom.target(IURLSegment)
class IJavascriptFolderAdaptor(object):
    def __init__(self,context):
        self.context=context   

    def getSegment(self):
        return 'search'
    
