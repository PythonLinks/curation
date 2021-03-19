from . import tal_template
from zope import interface
from zope import schema
from zope.interface import Interface

from dolmen.container import IBTreeContainer,BTreeContainer
from cromlech.webob.response import Response
from zopache.core.page import Page
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.core.getroot import getProducts
from zopache.core.viewdecorators import *
from zopache.core import Leaf
from zopache.ttw.acescripts import AceScripts as AceScriptsBase
from zopache.ttw.interfaces import ISourceLeaf, ISourceContainer
from zopache.core.interfaces import ITreeSecurity

class ISass(ISourceLeaf):
    title = schema.TextLine(
        title = u'Title',
        description = u'Describe this Sass  Object.',
        required = False,
    )

    source= schema.Text(
        title = u'Sass Source Code',
        description = 'The Sass code goes here.',
        required = False,
        default = u' ',
    )

    #THIS IS JUST TO WORK LIKE COFFEESCRIPT
    javascript = schema.Text(
        title = 'The Generated css',
        description = 'This CSS is generated from the Sass',
        required = False,
        default = u'',
    )    

@implementer(ISass)      
class Sass(Leaf):
    icon="ttwicons/CSS.svg"    
    source =u''
    title=u''

from .css import makeCSSResponse, makeSassResponse, makeScSSResponse

@view_component
@name('index')
@context(ISass)
class CSSIndex(Page):
    responseFactory = Response
    make_response = makeCSSResponse
        
    def render(self ):
        # TO WORK LIKE COFFEESCRIPT
        return self.context.javascript

@view_component
@name('sassIndex')
@context(ISass)
class SassIndex(Page):
    responseFactory = Response
    make_response = makeSassResponse
        
    def render(self ):
        # TO WORK LIKE COFFEESCRIPT
        return self.context.source

    
class  AceScripts(AceScriptsBase):
    aceMode = 'sass'

    def update(self):
        self.template = getProducts(self)['Templates']['TranspilerTemplate']
        super().update()
        
    def  footerScripts(self):
        result =  AceScriptsBase.footerScripts(self)         
        result += """
<script  src="/fanstatic/ttwicons/sass.js"></script>
    """
        result += "<script>"
        script = getProducts(self)['Templates']['TranspilerScripts']
        result += """
                  var transpiler = 'Sass';
                  """
        result += script.source
        result += "</script>"
        return result

@form_component
@name('addSass')
@context(IBTreeContainer)
@target(IView)
@implementer(ITreeSecurity)
class AddSass(AceScripts,AceAddForm):
    aceMode = "sass"
    title = "Create a Sass object"
    subTitle='Add a Sass Object'
    interface = ISass
    ignoreContent = True
    factory=Sass

    
#HERE WE HAVE THE ACE EDIT FORM               
@form_component
@context(ISass)
@target(IView)
@name("aceedit")
@implementer(ITreeSecurity)
class EditSass(AceScripts,AceEditForm):
    subTitle = "Ace Edit a Sass Object."
    title = "Sass Editor"
    aceMode = "sass"
    
import crom
from zopache.zmi.interfaces import IURLSegment
@crom.adapter
@crom.sources(ISass)
@crom.target(IURLSegment)
class ISassAdaptor(object):
    def __init__(self,context):
        self.context=context   

    def getSegment(self):
        return 'aceedit'
