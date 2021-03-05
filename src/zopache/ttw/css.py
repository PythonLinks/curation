#This software is subject to the No Compete MIT license License Agreement.

from zopache.core.viewdecorators import *
from zope import schema
from cromlech.webob.response import Response

from dolmen.view import View, make_view_response

from dolmen.container import IBTreeContainer

from zopache.ttw.interfaces import IGrapeBase
from zopache.core import Leaf
from zopache.ttw.interfaces import ISourceLeaf, ISearchable
from zopache.ttw.interfaces import ITestSource as ISource
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.crud.forms import EditDemoForm
from zope.interface import Interface
from zopache.ttw.javascript import JavascriptBase, JavascriptFolderBase
from zopache.core.interfaces import ITreeSecurity
from dolmen.container import IBTreeContainer
from zopache.ttw.interfaces import IAceDiff
from zopache.ttw.acescripts import AceScripts
from zopache.core.page import Page

class ICSSBase(IAceDiff):
    """ For CSS Leaves and Folders."""
    pass

class ICSSFolder(ICSSBase, ISearchable,  IBTreeContainer):
    """ For CSS Leaves and Folders."""
    pass

class ICSS(ICSSBase, ISourceLeaf):
    """Basic CSS CRUD"""

    title = schema.TextLine(
        title = u'Title',
        description = u'Please Describe this CSS.',
        required = False,
    )

    source= schema.Text(
        title = u'CSS Source Code',
        description = u'The CSS goes here.',
        required = False,
        default = u'',
    )


@implementer(ICSS)
class CSS(JavascriptBase,Leaf):
    icon="ttwicons/CSS.svg"
    aceMode = 'css'
    englishType = 'CSS'

class  AceScripts(AceScripts):
     aceMode = 'css'
    

@form_component
@name('addCSS')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddCSS(AceScripts,AceAddForm):
    subTitle='Add a CSS Object'
    interface = ICSS
    ignoreContent = True
    factory=CSS
    

def makeCSSResponse(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or u'')
        response.content_type=u'text/css'
        return response

def makeSassResponse(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or u'')
        response.content_type=u'text/x-sass'
        return response

def makeScSSResponse(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or u'')
        response.content_type=u'text/x-scss,'
        return response        

@view_component
@name('index')
@context(ICSSBase)
class Index(View):
    responseFactory = Response
    make_response = makeCSSResponse
        
    def render(self):
               return self.context.getJavascript()

    
@view_component
@name('css')
@context(IGrapeBase)
class ShowGrapeCSS(View):
    responseFactory = Response
    make_response = makeCSSResponse
        
    def render(self):
               return self.context.css    



#AND HERE IS THE ACE DEMO FORM

#HERE IS THE ACE EDIT FORM
@form_component
@context(ICSS)
@name('acedemo')
class AceDemoCSS(AceScripts,EditDemoForm):
    subTitle='Edit a CSS Object, saving disabled'



#HERE IS THE ACE EDIT FORM
@form_component
@context(ICSS)
@name('aceedit')
class AceEditCSS(AceScripts,AceEditForm):
    subTitle='Edit a CSS Object'

from zopache.core.breadcrumbs import Breadcrumbs
from zopache.crud.forms import EditForm
@form_component
@context(IAceDiff)
@name('acediff')
class AceDiff(EditForm,Breadcrumbs):
    layoutName = "NoMenu"
    subTitle = '<center>If you have permission, you can save them.</center>'
    def update(self):
        self.title=F'<center>Diff two {self.context.englishType} Objects</center>'    
        templates = self.getTemplates()
        self.template = templates['AceDiff']
        super().update(self)


@implementer(ICSSFolder)
class CSSFolder(JavascriptFolderBase,CSS):
    className='CSSFolder'
    icon="ttwicons/CSS.svg"    
    title = ""
    
    def getCompressedCode(self):
        return self.getJavascript()
    
    def getJavascript(self):
        result =  ' '
        for item in self.values():
            if ICSS.providedBy(item):
                result +=item.getJavascript()
                result += '\n'
        return result

from zopache.ttw.addeditforms import AddAndSearchForm    
from zopache.ttw.interfaces import IName, IContainer, ILeaf    
@form_component
@name('addCSSFolder')
@context(IBTreeContainer)
@target(IView)
@implementer(ITreeSecurity)
class AddCSSFolder(AceScripts,AddAndSearchForm):
    title= 'Add a CSS Folder'
    subTitle = 'To organize multiple CSS objects'
    interface = IContainer
    ignoreContent = True
    factory=CSSFolder    

@view_component
@name('.scss')
@context(ICSS)
class SCSSIndex(Page):
    responseFactory = Response
    make_response = makeScSSResponse
        
    def render(self ):
        return self.context.source

    
        
import crom
from zopache.zmi.interfaces import IURLSegment
@crom.adapter
@crom.sources(ICSSFolder)
@crom.target(IURLSegment)
class ICSSFolderAdaptor(object):
    def __init__(self,context):
        self.context=context   

    def getSegment(self):
        return 'manage'
