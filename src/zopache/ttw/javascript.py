from jsmin import jsmin
from . import tal_template
from html import escape
from zope import interface
from zope import schema
from zope.schema.interfaces import IField
from zope.interface import Interface
from zopache.ttw.interfaces import ITestSource as ISource
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from dolmen.container import IBTreeContainer
from zopache.crud.forms import EditDemoForm
from zopache.core.viewdecorators import *
from dolmen.container import IBTreeContainer,BTreeContainer
from zopache.core import Leaf
from zopache.ttw.acescripts import AceScripts
from .interfaces import ISourceContainer
from zopache.ttw.interfaces import ISourceLeaf, ISourceContainer
from zopache.ttw.interfaces import IWeb
from zopache.core.page  import  Page
from .interfaces import ITestURL
from cromlech.webob.response import Response
class IJavascript(ISourceLeaf,ITestURL):
    "Basic Javascript Form"

    title = schema.TextLine(
        title = u'Title',
        description = u'Describe this Javascript Object.',
        required = False,
    )

    source= schema.Text(
        title = u'Javascript Source Code',
        description = u'The Javascript code goes here.',
        required = False,
        default = u' ',
    )

class IJavascriptFolder(IJavascript,IBTreeContainer,ISourceContainer):
        "Basic Javascript Folder Form"
        pass
        

class JavascriptBase(object):
    def getSource(self):
        return self.source

    def getJavascriptObjects(self):
         return [self]

    def getLines(self):
         #NOT QUITE SURE WHAT THE FOLLOWING LINE WAS THERE.
         #result=self.source.replace(' ','mynbsp')
         result=self.getSource()
         result=escape(result)
         #result=result.replace('mynbsp','&nbsp')
         return result.split("\n")
    
    def getTitle(self):
        return self.__name__

    def postProcess(self):
        self.createJavascriptCaches()

    def postAddProcess(self):
        self.postProcess()

    def createJavascriptCaches(self):
        parentJavascriptFolders=self.parentsWhichImplement(IJavascriptFolder)
        for folder in parentJavascriptFolders:
             folder.sourceCache=jsmin(folder.getSource())

    def parentsWhichImplement(self,interface):
           item=self
           result=[]
           while (item!=None):
             if interface.providedBy(item):
                       result.append(item)
             item=item.__parent__
           return result

    def __call__(self,view,**args):
            return self.getSource()       
    
@implementer(IJavascript)      
class Javascript(JavascriptBase,Leaf):
    icon="ttwicons/Javascript.svg"    
    source =u''
    title=u''
    className='Javascript'
                
@implementer(IJavascriptFolder)
class JavascriptFolder(Javascript,BTreeContainer):
    source =u''
    sourceCache=u''
    className='Javascript Folder'

    def cacheSource(self):
        self.sourceCache=self.getSource()

    def getSource(self):
        if self.source!=None:
          result=self.source
        else:
          result=u' '  
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


class  AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/javascript");
        </script>
        """     

    def commands(self):
        manual=self.liHref('http://www.zopache.com/baseicwebobjects/javascript','Javascript Manual')
        return manual 

@form_component
@name('addJavascript')
@context(IBTreeContainer)
@target(IView)
@title("Add Javascript")
@permissions('Manage')
@implementer(IWeb)
class AddJavascript(AceScripts,AceAddForm):
    subTitle='Add a Javascript Object'
    interface = IJavascript
    ignoreContent = True
    factory=Javascript

    def postProcess(self):
        self.new.postProcess()


    
@form_component
@name('addJavascriptFolder')
@context(IBTreeContainer)
@target(IView)
@title("Add JavascriptFolder")
@permissions('Manage')
@implementer(IWeb)
class AddJavascriptFolder(AceScripts,AceAddForm):
    subTitle= 'Add a Javascript Folder'
    interface = IJavascriptFolder
    ignoreContent = True
    factory=JavascriptFolder    

    def postProcess(self):
        self.new.postProcess()
        
def make_javascript_response(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or u'')
        response.content_type=u'application/javascript' 
        return response

@view_component
@name('index')
@context(IJavascript)
@title("View Javascript")
class JavascriptIndex(Page):
    responseFactory = Response
    make_response = make_javascript_response
        
    def render(self ):
            if IJavascriptFolder.providedBy(self.context):
                   return self.context.sourceCache
            else: 
                   return self.context.source

class BaseJavascript(AceScripts):
    subTitle='Ace Edit this  Javascript'
    label=''
    def breadcrumbs(self):
        return self.breadcrumbsManage()
    
    def postProcess(self):
        self.context.postProcess()

    def footerScripts(self):
        return AceScripts.footerScripts(self)

    def headerScripts(self):
          return AceScripts.headerScripts(self)    
               
#HERE WE HAVE THE ACE EDIT FORM               
@form_component
@context(IJavascript)
@target(IView)
@title("AceEdit")
@name("aceedit")
@permissions('Manage')
class AceEditJavascript(BaseJavascript,AceEditForm):
    pass

#AND HERE WE HAVE THE ACE DEMO FORM               
@form_component
@context(IJavascript)
@target(IView)
@title("Ace Demo")
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

