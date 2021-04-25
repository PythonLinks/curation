from jinja2 import Template as JinjaTemplate
from zope import schema
from dolmen.container import IBTreeContainer
from cromlech.webob.response import Response
from zopache.core import View

from zopache.core import Leaf
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.core.viewdecorators import *
from zopache.ttw.interfaces import IJavascript, IJSON, IJinjaJSON, IJinjaJS
from zopache.ttw.interfaces import IJinjaHTML, IAceHTML
from zopache.ttw.acescripts import  AceScripts

class JinjaRecursionError(Exception):
        pass

class JinjaBase(Leaf):
    source = ''
    
    def postProcess(self,view = None):
        self.compileTemplate()

    #So here we pass the context into the template    
    def __call__(self,view,**args):
        try:
            view.count+= 1
            if view.count>500:
                raise JinjaRecursionError()
            context=view.context
            return self.callWithContext(view,context,**args)
        except AttributeError as error:
            result =  """COULD NOT DISPLAY THAT PAGE.
                      HERE IS THE ERROR MESSAGE:\n<br>"""
            result += str(error)
            return result
    
    def compileTemplate(self):
                 source=self.source
                 self._v_compiledTemplate = JinjaTemplate(source)

    def setTemplate(self):
            if not hasattr(self,'_v_compiledTemplate'):
               self.compileTemplate()
            
    def callWithContext(self,view,context,**args):
            self.setTemplate()
            result = self._v_compiledTemplate.render(
                           context=context,
                           request=view.request,
                           view=view,
                           **args)
            return result

@implementer(IJinjaJSON)
class JinjaJSON(JinjaBase):
    icon="ttwicons/JSON.svg"

@implementer(IJinjaJS)
class JinjaJS(JinjaBase):
    icon="ttwicons/Javascript.svg"        

@implementer(IJinjaHTML)
class JinjaHTML(JinjaBase):
    icon="ttwicons/HTML.svg"        
    
@form_component
@name('addJinjaJSON')
@context(IBTreeContainer)
@permissions('Manage')
class AddJinjaJSON(AceAddForm):
    aceMode = 'json'    
    title='Add a Jinja2 JSON Object'
    interface = IJSON
    ignoreContent = True
    factory=JinjaJSON
    def postAddProcess(self,view = None):
        self.new.compileTemplate()


@form_component
@name('addJinjaHTML')
@context(IBTreeContainer)
@permissions('Manage')
class AddJinjaHTML(AceAddForm):
    aceMode = 'html'    
    title='Add a Jinja2 HTML Object'
    interface = IAceHTML
    ignoreContent = True
    factory=JinjaHTML
    def postAddProcess(self,view = None):
        self.new.compileTemplate()        
        
@form_component
@name('addJinjaJS')
@context(IBTreeContainer)
@permissions('Manage')
class AddJinjaJS(AceAddForm):
    aceMode = 'javascript'
    title='Add a Jinja2 Javascript Object'
    interface = IJavascript
    ignoreContent = True
    factory=JinjaJS
    def postAddProcess(self,view = None):
        self.new.compileTemplate()


@form_component
@context(IJinjaJS)
@name("aceedit")
@permissions('Manage')
class AceEditJinjaJS(AceEditForm):
    aceMode = 'javascript'            
    title='Edit a JINJA Javascript Object'
    subtitle = "Jinja2 will be used to add in values"
    
@form_component
@context(IJinjaJSON)
@name("aceedit")
@permissions('Manage')
class AceEditJinjaJSON(AceEditForm):
    title='Edit a JINJA JSON Object'
    subtitle = "Jinja2 will be used to add in values"
    aceMode = 'json'
    
    def postProcess(self,view = None):
        self.context.compileTemplate()

@form_component
@context(IJinjaHTML)
@name("aceedit")
@permissions('Manage')
class AceEditJinjaHTML(AceEditForm):
    title='Edit a JINJA HTML Object'
    subtitle = "Jinja2 will be used to add in values"
    aceMode = 'html'
    
    def postProcess(self,view = None):
        self.context.compileTemplate()
        
from zopache.ttw.javascript import makeJavascriptResponse
from zopache.core.breadcrumbs import Breadcrumbs
from dolmen.view import  make_view_response

@view_component
@name('index')
@context(IJinjaJS)
class IndexJinjaJS(View,Breadcrumbs):
    count = 0    
    responseFactory = Response
    make_response = makeJavascriptResponse
    
    def setDisplayObject(self,item):
        self.zopacheTemplate = item
        return

    def render(self):
        context = self.context
        #In the case of /index/index
        if not hasattr(self,'zopacheTemplate'):
               self.zopacheTemplate=self.context
               self.context=self.context.__parent__        
        return self.zopacheTemplate.callWithContext(self,context)


@view_component
@name('index')
@context(IJinjaHTML)
class IndexJinjaHTML(View,Breadcrumbs):
    count = 0    
    responseFactory = Response
    make_response = make_view_response
    
    def setDisplayObject(self,item):
        self.zopacheTemplate = item
        return

    def render(self):
        context = self.context
        #In the case of /index/index
        if not hasattr(self,'zopacheTemplate'):
               self.zopacheTemplate=self.context
               self.context=self.context.__parent__        
        return self.zopacheTemplate.callWithContext(self,context)

from zopache.ttw.JSON import makeJsonResponse    
@view_component
@name('index')
@context(IJinjaJSON)
class IndexJinjaJSON(View,Breadcrumbs):
    responseFactory = Response
    make_response = makeJsonResponse
    count = 0        
    def setDisplayObject(self,item):
        self.zopacheTemplate=item
        
    def render(self):
        #In the case of /index/index
        if not hasattr(self,'zopacheTemplate'):
               self.zopacheTemplate=self.context
               self.context=self.context.__parent__
        context = self.context
        return self.zopacheTemplate.callWithContext(self,context)            



