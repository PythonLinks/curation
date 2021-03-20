from zope import schema

from dolmen.view import View, make_view_response
from dolmen.container import IBTreeContainer

from zopache.ttw.interfaces import IGrapeBase
from zopache.core.viewdecorators import *
from zopache.core import Container
from zopache.crud.forms import AddForm
from zopache.core.interfaces import ITreeSecurity
from zopache.ttw.interfaces import IAceHTML, IIndexHTML
from zopache.ttw.css import CSS
from zopache.ttw.javascript import Javascript
from zopache.crud.forms import EditForm
from zopache.core.breadcrumbs import Breadcrumbs
from zopache.pages.page import Page
from zopache.ttw.html import TrustedHTML


class IGrapePage(IGrapeBase):
      pass

class IGrapeLayout (IGrapeBase):
    pass

class GrapeBase(object):
    icon="ttwicons/HTML.svg"
    source = '{}'
    html = ''
    css = ''
    javascript = ''
    
    def getHTML(self):
        return self.html


@implementer(IGrapePage)
class GrapePage(GrapeBase,Page):
    webclass = "WikiPage"
    
    def render(self,extraArg,**args):
        css = self.renderCSS()
        core = self.renderHTML(self,extraArg,**args)
        javascript = self.renderJavascript()
        return css + core + javascript
    
    def renderHTML(self,extraArg,**args):
        if args['view'].isAuthenticated:
           return Page.render(self,extraArg,**args)
        else:
           return self.html
       
    def renderCSS(self):    
        if self.css !="":
            result = ""
            result += """ <link rel="stylesheet" 
                    type="text/css" href="""
            result += self.longURL( self)+ '/css'
            result += '">'
            return result
        
    def renderJavascript(self):
        result = ""
        if self.javascript != "":
           result += '<script src = "'
           result += self.longURL( self) +'/javascript'
           result +='"></script>'
        return result

    def size(self):
         return len (self)
     
#THE GRAPE PAGE CAN INCLUDE ITS CSS AND JAVASCRIPT
#THE LAYOUT HAS TO CALL IT EXPLICITELY. 
@implementer(IGrapeLayout)    
class GrapeLayout(GrapeBase,TrustedHTML,Container):
    def __init__(self):
        Container.__init__(self)
        
@form_component
@name('addGrapePage')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddGrape(AddForm,Breadcrumbs):
    subTitle='Add a Grape Object'
    interface = Interface
    ignoreContent = True
    factory=GrapePage
    def newURL(self,baseURL):
        return baseURL + '/edit'

@form_component
@name('addGrapeLayout')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddGrape(AddForm,Breadcrumbs):
    subTitle='Add a Grape Object'
    interface = Interface
    ignoreContent = True
    factory=GrapeLayout
    def newURL(self,baseURL):
        return baseURL + '/edit'    
    
from zopache.ttw.htmlviews import Index    
@view_component
@name('index')
@context(IGrapeLayout)
class IndexGrapeLayout(Index,Breadcrumbs):
    def render(self):   
       result = "<html>"

       result += F"""
   <link href="{self.getLongURL(self.context)}/css"
rel="stylesheet" 
/>
   <script
        src= "{self.getLongURL(self.context)}/js">
   </script>
    """
   
       result += "<Head>"
       result += "</Head>"
       result += Index.render(self)
       result += "</html>"   
       return result

from zopache.application.browser.viewlets import Tabs
class EditBase(EditForm,Breadcrumbs):
    def breadcrumbs(self):
        if self.treeSecurity():
           return self.breadcrumbsCore(
                        self.context,
                        viewName='manage',
                        showTitles=False,
                        showRoot=True
                        )
        else:
           result =  self.breadcrumbsCore(
                        self.context,
                        viewName='',
                        showTitles=True,
                        showRoot=False
                       ) 
           return result

    def renderMenuBar(self,layout):
        if self.treeSecurity():
           bootstrap = layout.bootstrap3()
           menuBar = Tabs.template.render(None,
                     request = self.request,
                      context=self.context,
                      view = self)
           return bootstrap + menuBar
     
        else:
           bootstrap = layout.bootstrap4()
           #menuBar = self.webClassAcquire('navbar.py', context = self.context.__parent__)(self)
           return bootstrap #+ menuBar
     
     
@form_component
@context(IGrapePage)
@name('edit')
class EditGrapePage(EditBase):
    layoutName = "ThinTop"
    title='Edit a Wiki Page' 
     #<a target="_blank"  href ="https://GrapesJS.com">GrapeJS</a> 
    def update(self):
       templates = self.getTemplates()
       self.template = templates["Grape-html"]
       super().update(self)
       
@form_component
@context(IGrapeBase)
@name('edit')
class EditGrapeLayout(EditBase):
    layoutName = "ThinTop"
    title='Edit a Layout Page'
    def update(self):
       templates = self.getTemplates()
       self.template = templates["Grape-html"]       
       super.update(self)
       

from cromlech.webob.response import Response
from dolmen.view import View, make_view_response
def make_jsx_response(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or u'')
        response.content_type=u'text/jsx'
        return response

from zopache.ttw.addeditforms import AceEditForm

@form_component
@context(IGrapeBase)
@name('aceedit')
@implementer(ITreeSecurity)
class AceEditGrape(AceEditForm):
    subTitle='Edit a Grape Object'
    aceMode = 'jsx'
       
import crom
from zopache.zmi.interfaces import IURLSegment
@crom.adapter
@crom.sources(IGrapeBase)
@crom.target(IURLSegment)
class IGrapeAdaptor(object):
    def __init__(self,context):
        self.context=context   

    def getSegment(self):
        return 'edit'
    
"""
    def getCSS(self):
        if "grape.css" in self:
            self["grape.css"].source
        else:
           return ''
       
    def setCSS(self,value):
        if not "grape.css" in self:
           new = CSS()
           self ["grape.css"] = new
           new.__parent__ = self
           new.__name__ = "grape.css"
           self ["grape.css"] = new 
        self ["grape.css"] = self
        
    def getJavascript(self):
        if "grape.js" in self:
           return self["grape.js"].source
        else:
           return ''
       
    def setJavascript(self,value):
        if not "grape.js" in self:
           new = Javascript()
           self ["grape.js"] = new
           new.__parent__ = self
           new.__name__ = "grape.js"
           self ["grape.css"] = new 
        self ["grape.js"] = self
        
    css = property(getCSS,setCSS)
    javascript = property(getJavascript,setJavascript)
    """
    
