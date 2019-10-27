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

class IReact(ISourceLeaf,IJavascript,ITestURL):
    "Basic React Form"

    title = schema.TextLine(
        title = u'Title',
        description = u'Describe this React g Object.',
        required = False,
    )

    source= schema.Text(
        title = u'React Source Code',
        description = u'The React code goes here.',
        required = False,
        default = u' ',
    )
    javascript= schema.Text(
        title = u'The Generated React',
        description = u'This Javascript is generated from the React',
        required = False,
        default = u'',
    )    

from .javascript import JavascriptBase    
@implementer(IReact)      
class React(JavascriptBase,Leaf):
    icon="ttwicons/React.svg"    
    source =u''
    title=u''
    className='React'

    def getJavascript(self):
        return self.javascript

    def getSource(self):
        return self.source

class  AceScripts(AceScriptsBase):
    def update(self):
        products = self.getProducts()
        self.template = products ['Templates']['TranspilerTemplate']
        
    def  headerScripts(self):
        result = AceScriptsBase.headerScripts(self)
        return result        
    
    def  footerScripts(self):
        result =  self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/react");
        </script>
        """     
        result += """
<script  src="https://unpkg.com/babel-standalone@6.26.0/babel.min.js"></script>
    """
        result += "<script>"
        products= self.getProducts()
        script =  products ['Templates']['TranspilerScripts']
        result += """
                  var transpiler = 'React';
                  """
        result += script.source
        result += "</script>"
        return result

@form_component
@name('addReact')
@context(IBTreeContainer)
@target(IView)
@title("Add React")
@permissions('Manage')
@implementer(IWeb)
class AddReact(AceScripts,AceAddForm):
    subTitle='Add a React Object'
    interface = IReact
    ignoreContent = True
    factory=React

    def postProcess(self):
        self.new.postProcess()

            
from .javascript import make_javascript_response, JavascriptBase

@view_component
@name('index')
@context(IReact)
@title("View React")
class ReactIndex(Page):
    responseFactory = Response
    make_response = make_javascript_response
        
    def render(self ):
        return self.context.javascript

class BaseReactForm(AceScripts):
    subTitle='Ace Edit this  React Object'
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
@context(IReact)
@target(IView)
@title("AceEdit")
@name("aceedit")
@permissions('Manage')
class AceEditReact(BaseReactForm,AceEditForm):
    subTitle = "Ace Edit a React Object."
    title = "React Editor"

#AND HERE WE HAVE THE ACE DEMO FORM               
@form_component
@context(IReact)
@target(IView)
@title("Ace Demo")
@name("acedemo")
class AceDemoReact(BaseReactForm,EditDemoForm):
    subTitle = "Ace Edit React  Demo."        
