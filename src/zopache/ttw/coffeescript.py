from jsmin import jsmin
from . import tal_template
from html import escape
from zope import interface
from zope import schema
from zope.schema.interfaces import IField
from zope.interface import Interface

from dolmen.container import IBTreeContainer,BTreeContainer
from dolmen.container import IBTreeContainer
from cromlech.webob.response import Response


from zopache.ttw.interfaces import ITestSource as ISource
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.crud.forms import EditDemoForm
from zopache.core.getroot import getProducts

from .interfaces import IJavascript
from zopache.core.viewdecorators import *
from zopache.core import Leaf
from zopache.ttw.acescripts import AceScripts as AceScriptsBase
from .interfaces import ISourceContainer
from zopache.ttw.interfaces import ILeaf, ISourceContainer
from zopache.core.page  import  Page
from .javascript import JavascriptBase
from zopache.core.interfaces import ITreeSecurity

class ICoffeeScript(ILeaf,IJavascript):
    "Basic CoffeeScript Form"

    title = schema.TextLine(
        title = u'Title',
        description = u'Describe this CoffeeScript Object.',
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
    icon="ttwicons/CoffeeScript.svg"    
    source =u''
    title=u''
    className='CoffeeScript'

    def getJavascript(self):
        return self.javascript

    def getSource(self):
        return self.source

class  AceScripts(AceScriptsBase):
    aceMode = 'coffee'
    def update(self):
        self.template = getProducts(self)['Templates']['TranspilerTemplate']
        super().update()
        
    def  footerScripts(self):
        result =  AceScriptsBase.footerScripts(self) 
        result += """
<script  src="/fanstatic/ttwicons/coffeescript.js"></script>
    """
        result += "<script>"
        script = getProducts(self)['Templates']['TranspilerScripts']
        result += """
                  var transpiler = 'CoffeeScript';
                  """
        result += script.source
        result += "</script>"
        return result

            
from .javascript import makeJavascriptResponse, JavascriptBase

@view_component
@name('index')
@context(ICoffeeScript)
@title("View CoffeeScript")
class CoffeeScriptIndex(Page):
    responseFactory = Response
    make_response = makeJavascriptResponse
        
    def render(self ):
        return self.context.javascript

class AceScripts2(AceScripts):
    aceMode = "coffee"
    def breadcrumbs(self):
        return self.breadcrumbsManage()
    

@form_component
@name('addCoffeeScript')
@context(IBTreeContainer)
@target(IView)
@title("Add CoffeeScript")
@implementer(ITreeSecurity)
class AddCoffeeScript(AceScripts2,AceAddForm):
    subTitle='Add a Coffeecript Object'
    interface = ICoffeeScript
    ignoreContent = True
    factory=CoffeeScript

    
#HERE WE HAVE THE ACE EDIT FORM               
@form_component
@context(ICoffeeScript)
@target(IView)
@title("AceEdit")
@name("aceedit")
@implementer(ITreeSecurity)
class AceEditCoffeeScript(AceScripts2,AceEditForm):
    subTitle = "Ace Edit a Coffescript Object."
    title = "CoffeeScript Editor"

