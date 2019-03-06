from jsmin import jsmin
from . import tal_template
from html import escape
from zope import interface
from zope import schema
from zope.schema.interfaces import IField
from zope.interface import Interface
from zopache.ttw.interfaces import ITestSource as ISource
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.crud.forms import EditDemoForm
from dolmen.container import IBTreeContainer
from .interfaces import IJavascript
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

class ICoffeeScript(ISourceLeaf,IJavascript,ITestURL):
    "Basic CoffeeScript Form"

    title = schema.TextLine(
        title = u'Title',
        description = u'Describe this CoffeeScript g Object.',
        required = False,
    )

    source= schema.Text(
        title = u'CoffeeScript Source Code',
        description = u'The CoffeeScript code goes here.',
        required = False,
        default = u' ',
    )
    javascript= schema.Text(
        title = u'The Generated CoffeeScript',
        description = u'This Javascript is generated from the CoffeeScript',
        required = False,
        default = u'',
    )    

from .javascript import JavascriptBase    
@implementer(ICoffeeScript)      
class CoffeeScript(JavascriptBase,Leaf):
    icon="ttwicons/Javascript.svg"    
    source =u''
    title=u''
    className='CoffeeScript'

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
        <script >editor.getSession().setMode("ace/mode/coffee");
        </script>
        """     
        result += """
<script  src="https://pythonlinks.info/static/coffeescript/coffeescript.js"></script>
    """
        result += "<script>"
        root= self.getRoot()
        script = root['Products']['Templates']['CoffeeScriptScripts']
        result += script.source
        result += "</script>"
        return result

@form_component
@name('addCoffeeScript')
@context(IBTreeContainer)
@target(IView)
@title("Add CoffeeScript")
@permissions('Manage')
@implementer(IWeb)
class AddCoffeeScript(AceScripts,AceAddForm):
    subTitle='Add a Coffeecript Object'
    interface = ICoffeeScript
    ignoreContent = True
    factory=CoffeeScript

    def postProcess(self):
        self.new.postProcess()

            
from .javascript import make_javascript_response, JavascriptBase

@view_component
@name('index')
@context(ICoffeeScript)
@title("View CoffeeScript")
class CoffeeScriptIndex(Page):
    responseFactory = Response
    make_response = make_javascript_response
        
    def render(self ):
        return self.context.javascript

class BaseCoffeeScriptForm(AceScripts):
    subTitle='Ace Edit this  Coffeecript'
    label=''
    def breadcrumbs(self):
        return self.breadcrumbsManage()
    
    def postProcess(self):
        self.context.postProcess()

    #def footerScripts(self):
    #    return AceScriptsBase.footerScripts(self)

    #def headerScripts(self):
    #      return AceScripts.headerScripts(self)    
               
#HERE WE HAVE THE ACE EDIT FORM               
@form_component
@context(ICoffeeScript)
@target(IView)
@title("AceEdit")
@name("aceedit")
@permissions('Manage')
class AceEditCoffeeScript(BaseCoffeeScriptForm,AceEditForm):
    subTitle = "Ace Edit a Coffescript Object."
    title = "CoffeeScript Editor"

#AND HERE WE HAVE THE ACE DEMO FORM               
@form_component
@context(ICoffeeScript)
@target(IView)
@title("Ace Demo")
@name("acedemo")
class AceDemoCoffeecript(BaseCoffeeScriptForm,EditDemoForm):
    subTitle = "Ace Edit Coffescript Demo."        
