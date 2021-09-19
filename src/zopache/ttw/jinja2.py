import sys
import jinja2
from jinja2 import Environment
from jinja2.sandbox import SecurityError
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
from zopache.copy import copy
from zopache.core.interfaces import ITreeSecurity
from zopache.core.relatives import Parents
from zopache.application.sandbox import MyEnvironment, LoadTemplate
from zopache.core.relatives import parentWhichImplements
from zopache.ttw.interfaces import IInternalPrincipal

class JinjaRecursionError(Exception):
        pass

class JinjaBase(Leaf):
    source = ''
    trusted = False    
    def postProcess(self,view = None):
        self.compileTemplate(view)
	
    def postAddProcess(self,view = None):
        self.postProcess(view = view)

    def postProcess(self,view = None):
        self.trusted = view.isManager()
        if hasattr(self, '_v_compiledTemplate'):
           del self._v_compiledTemplate
        self.compileTemplate(view)

	
    #So here we pass the context into the template    
    def __call__(self,view,**args):
            view.count+= 1
            if view.count>500:
                raise JinjaRecursionError()
            context=view.context
            return self.callWithContext(view,context,**args)
    
    def compileTemplate(self,view):
         base = self.parentalPrincipal() or view.getLayout()
         #if hasattr(base,"_v_environment"):         
         #  if hasattr(self,"_v_compiledTemplate"):
         #    return self._v_compiledTemplate
         loadTemplate = LoadTemplate()
         loader = jinja2.FunctionLoader(loadTemplate)                 
         if self.trusted:
            environment = Environment(loader = loader)
         else:
            environment = MyEnvironment(loader = loader)
         loadTemplate.parent = environment
         environment.parent = base
         base._v_environment = environment
         source=self.source
         self._v_compiledTemplate = environment.from_string(source)

    def setTemplate(self,view):
            if not hasattr(self,'_v_compiledTemplate'):
               self.compileTemplate(view)
	       
    def callWithContext(self,view,context,**args):

            self.setTemplate(view)
            request = view.request
            #try:
            ctx = {
                               "view": view,
                               "node" : context,
                               "request" : request}
                    
            result =  self._v_compiledTemplate.render(context = ctx,
                                                          node = context,
                                                          view= view,
                                                          request = request)
            return result
            try:
                    pass
            except AttributeError as error:
               result =  """COULD NOT DISPLAY THAT PAGE.
                      HERE IS THE ERROR MESSAGE:\n<br>"""
               result += str(error)
               return result

                                                          
            except SecurityError as error:
                result =  """JINJA REPORTED THIS SECURITY ERROR: \n<br>"""
                result += str(error)
                return result
        
            except:
                error  = sys.exc_info()[0]
                result =  """COULD NOT DISPLAY THAT PAGE.
                      HERE IS THE ERROR MESSAGE:\n<br>"""
                strError = str(error).replace("<"," ").replace(">"," ")
                return result + strError
    
    def parentalPrincipal(self):
        return parentWhichImplements (self,IInternalPrincipal)               


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
@implementer(ITreeSecurity)
class AddJinjaJSON(AceAddForm):
    aceMode = 'json'    
    title='Add a Jinja JSON Object'
    interface = IJSON
    ignoreContent = True
    factory=JinjaJSON


@form_component
@name('addJinjaHTML')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddJinjaHTML(AceAddForm):
    aceMode = 'html'    
    title='Add a Jinja HTML Object'
    interface = IAceHTML
    ignoreContent = True
    factory=JinjaHTML
        
@form_component
@name('addJinjaJS')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddJinjaJS(AceAddForm):
    aceMode = 'javascript'
    title='Add a Jinja Javascript Object'
    interface = IJavascript
    ignoreContent = True
    factory=JinjaJS

@form_component
@context(IJinjaJS)
@name("aceedit")
@implementer(ITreeSecurity)
class AceEditJinjaJS(AceEditForm):
    aceMode = 'javascript'            
    title='Edit a JINJA Javascript Object'
    subtitle = "Jinja will be used to add in values"
    
@form_component
@context(IJinjaJSON)
@name("aceedit")
@implementer(ITreeSecurity)
class AceEditJinjaJSON(AceEditForm):
    title='Edit a JINJA JSON Object'
    subtitle = "Jinja will be used to add in values"
    aceMode = 'json'
    
@form_component
@context(IJinjaHTML)
@name("aceedit")
@implementer(ITreeSecurity)
class AceEditJinjaHTML(AceEditForm):
    title='Edit a JINJA HTML Object'
    subtitle = "Jinja will be used to add in values"
    aceMode = 'html'
    
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



