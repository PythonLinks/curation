from jsmin import jsmin
from . import tal_template
from html import escape
from zope import interface
from zope import schema
from zope.schema.interfaces import IField
from zope.interface import Interface
from zopache.ttw.interfaces import ITestSource as ISource
from zopache.ttw.addeditforms import AceAddForm, PugEditForm
from zopache.crud.forms import EditDemoForm
from dolmen.container import IBTreeContainer

from zopache.core.viewdecorators import *
from dolmen.container import IBTreeContainer,BTreeContainer
from zopache.core import Leaf
from zopache.ttw.acescripts import AceScripts as AceScriptsBase
from .interfaces import ISourceContainer
from zopache.ttw.interfaces import ISourceLeaf, ISourceContainer
from zopache.ttw.interfaces import IWeb
from zopache.core.page  import  Page
from .interfaces import ITestURL
from cromlech.webob.response import Response
from .javascript import JavascriptBase
from dolmen.view import View, make_view_response

class IPugBase(ISourceLeaf):
    pass
  
class IPug(IPugBase):    
    "Basic Pug Form"

    title = schema.TextLine(
        title = u'Title',
        description = u'Describe this Pug g Object.',
        required = False,
    )

    globals = schema.TextLine(
        title = u'Globals',
        description = u'Which Global Variables are Accessible',
        required = False,
    )    

    source= schema.Text(
        title = u'Pug Source Code',
        description = u'The Pug Template:',
        required = False,
        default = u' ',
    )
    
    javascript= schema.Text(
        title = u'Javascript',
        description = u'The generated Javascript:',
        required = False,
        default = u'',
    )
    
    html= schema.Text(
        title = u'HTML:',
        description = u'The generated HTML:',
        required = False,
        default = u'',
    )
    
from .javascript import JavascriptBase    
@implementer(IPug)      
class Pug(JavascriptBase,Leaf):
    icon="ttwicons/Javascript.svg"    
    source =u''
    title=u''
    className='Pug'

    def getJavascript(self):
        return self.javascript

    def getSource(self):
        return self.source

class  AceScripts(AceScriptsBase):
    def update(self):
        root = self.getRoot()
        self.template = root['Products']['Templates']['CoffeeScriptTemplate']
        
    def  headerScripts(self):
        result = AceScriptsBase.headerScripts(self)
        return result        
    
    def  footerScripts(self):
        result =  self.aceEditorFooter + """
        <script >editor.getSession().setMode("ace/mode/jade");</script>
 
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.9.0-beta3/beautify.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.9.0-beta3/beautify-html.min.js"></script>
        """     
        result += """
<script  src="https://pythonlinks.info/static/pug/pug.js"></script>
<script  src="https://pythonlinks.info/static/pug/runtime.js"></script>    
        """
        result += "<script>"
        root= self.getRoot()
        script = root['Products']['Templates']['PugScripts']
        result += script.getJavascript()
        result += "</script>"
        return result

            

class BasePugForm(AceScripts):
    label=''
    def breadcrumbs(self):
        return self.breadcrumbsManage()
    
    def postProcess(self):
        self.context.postProcess()

@form_component
@name('addPug')
@context(IBTreeContainer)
@target(IView)
@title("Add Pug")
@permissions('Manage')
@implementer(IWeb)
class AddPug(AceScripts,AceAddForm):
    subTitle='Add a Pug Object'
    interface = IPug
    ignoreContent = True
    factory=Pug

    def postProcess(self):
        self.new.postProcess()


        
#HERE WE HAVE THE ACE EDIT FORM               
@form_component
@context(IPug)
@target(IView)
@title("AceEdit")
@name("aceedit")
@permissions('Manage')
class AceEditPug(BasePugForm,PugEditForm):
    subTitle='Ace Edit this Pug Template.'
    pass

#AND HERE WE HAVE THE ACE DEMO FORM               
@form_component
@context(IPug)
@target(IView)
@title("Ace Demo")
@name("acedemo")
class AceDemoPug(BasePugForm,EditDemoForm):
    def breadcrumbs(self):
        return self.breadcrumbsIndex(self.context)
    
        

#RENDER HTML
from .html import make_view_response
@view_component
@name('index')
@context(IPug)
@title("View Pug  HTML")
class PugIndexHTML(View):
    responseFactory = Response
    make_response = make_view_response
        
    def render(self):
               return self.context.html

from .javascript import make_javascript_response, JavascriptBase

@view_component
@name('javascript')
@context(IPug)
@title("View Pug")
class PugJavascipt(Page):
    responseFactory = Response
    make_response = make_javascript_response
        
    def render(self ):
        return self.context.javascript
