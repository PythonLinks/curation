from jinja2 import Template as JinjaTemplate
from zope import schema
from dolmen.container import IBTreeContainer
from cromlech.webob.response import Response
from zopache.core import View

from zopache.core import Leaf
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.core.viewdecorators import *
from zopache.ttw.interfaces import IJavascript, IJSON, IJinjaJSON, IJinjaJS
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

@form_component
@name('addJinjaJSON')
@context(IBTreeContainer)
@permissions('Manage')
class AddJinjaJSON(AceAddForm):
    acemode = 'json'    
    title='Add a Jinja2 JSON Object'
    interface = IJSON
    ignoreContent = True
    factory=JinjaJSON
    def postAddProcess(self,view = None):
        self.new.compileTemplate()
        
@form_component
@name('addJinjaJS')
@context(IBTreeContainer)
@permissions('Manage')
class AddJinjaJS(AceAddForm):
    acemode = 'javascript'
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
    acemode = 'javascript'            
    title='Edit a JINJA Javascript Object'
    subtitle = "Jinja2 will be used to add in values"
    
@form_component
@context(IJinjaJSON)
@name("aceedit")
@permissions('Manage')
class AceEditJinjaJSON(AceEditForm):
    title='Edit a JINJA JSON Object'
    subtitle = "Jinja2 will be used to add in values"
    acemode = 'json'
    
    def postProcess(self,view = None):
        self.context.compileTemplate()
    
from zopache.ttw.javascript import makeJavascriptResponse
from zopache.core.breadcrumbs import Breadcrumbs

@view_component
@name('index')
@context(IJinjaJS)
class IndexJinjaJS(View,Breadcrumbs):
    count = 0    
    responseFactory = Response
    make_response = makeJavascriptResponse
    
    def setDisplayObject(self,item):
        self.zopacheTemplate=item
        
    def render(self):
        context = self.context    
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
        context = self.context    
        return self.zopacheTemplate.callWithContext(self,context)            



