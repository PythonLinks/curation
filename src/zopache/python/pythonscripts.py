#sheThis software is subject to the CV License Agreement
from zope.schema import ValidationError
from dolmen.forms.base import Actions
from zopache.crud   import i18n as _
from zopache.crud.actions import Cancel
from zopache.ttw import actions  as ttwactions
from zopache.crud.actions import Add,Edit
from zope import interface
from zope import schema
from zope.schema.interfaces import IField
from zope.interface import Interface
from zopache.ttw.interfaces import ISource
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zope.interface import implementer
from dolmen.forms.base import action, name, context, form_component
from dolmen.container import IBTreeContainer
from crom import target, order
from cromlech.browser.directives import title
from cromlech.security import permissions
from zopache.core import Leaf
from zopache.ttw.interfaces import IWeb
from dolmen.view import name, context, view_component
from dolmen.view import View
from cromlech.webob.response import Response
from dolmen.view import View, make_view_response
from zope.cachedescriptors.property import CachedProperty
from RestrictedPython import compile_restricted_function
from RestrictedPython import compile_restricted
from zopache.python.acescripts import AceScripts
from RestrictedPython import safe_builtins, utility_builtins, limited_builtins
from RestrictedPython import RestrictingNodeTransformer
from zopache.ttw.interfaces import ITestURL
from zopache.python.interfaces import IPython
from zopache.core.getroot import getRoot
from zopache.core.breadcrumbs import parents

import RestrictedPython
from RestrictedPython import _compat
from dolmen.forms.base.interfaces import ActionError

def safer_getattr(object, name, default=None, getattr=getattr):
    """Getattr implementation which prevents using format on string objects.

    format() is considered harmful:
    http://lucumr.pocoo.org/2016/12/29/careful-with-str-format/

    """
    if isinstance(object, _compat.basestring) and name == 'format':
        raise NotImplementedError(
            'Using format() on a %s is not safe.' % object.__class__.__name__)
    return getattr(object, name, default)


safe_builtins['_getattr_'] = getattr
#safe_builtins['_iter_unpack_sequence_'] = RestrictedPython.Guards.guarded_iter_unpack_sequence
from RestrictedPython.Guards import guarded_iter_unpack_sequence

def default_guarded_getiter(ob):
        # No restrictions.
        return ob
    
def default_guarded_getitem(ob, index):
        # No restrictions.
        return ob[index]

safe_locals = {}
    
class OwnRestrictingNodeTransformer(RestrictingNodeTransformer):
        pass

policy = OwnRestrictingNodeTransformer

policy_instance = OwnRestrictingNodeTransformer(
            errors=[],
            warnings=[],
            used_names=[]
        )



class  DotAccess(object):
        
    def __init__(self, context):
        self.context = context
        
    def __getattr__(self, name):
        if name in self.context:
            item =  self.context[name]
            if IPython.providedBy(item):
               return item
            return DotAccess(item)
        item = object.__getattr__(self, name)
        return item



@implementer(IPython)
class PythonScript(Leaf):
    icon="ttwicons/Python.svg"
    
    def dotAccessParents(self):
        theParents = parents (self)
        #result =  dict((node.__name__,DotAccess(node) ) for node in theParents)
        result =  dict((node.__name__,node ) for node in theParents)        
        return result

    
    #We could save some cycles and only compile this when loaded from the ZODB
    def getCode(self):
       if not hasattr(self,'_v_code'):
          self.compile()
       return self._v_compiledFunction

    def postProcess(self):
            self.compile()
            
    def compile(self):
        compiled = compile_restricted_function(
            self.arguments,
            self.source,
            self.__name__,
            globalize = ['view'])
        self._v_code=compiled.code
        self._v_errors=compiled.errors
        self._v_warnings=compiled.warnings
        self._v_used_names=compiled.used_names
        products = self.dotAccessParents()
        safe_globals = {**safe_builtins, 
                        **limited_builtins, 
                        **utility_builtins,
                        **products}
        safe_globals['_getiter_']  = default_guarded_getiter
        safe_globals['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence
        safe_globals['_getitem_'] = default_guarded_getitem
        
        exec(compiled.code, safe_globals, safe_locals)
        self._v_compiledFunction = safe_locals[self.__name__]
    
    def __call__(self,*args, **kwargs):
        code=self.getCode()
        return code(*args,**kwargs)


class  AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/python");
        </script>
        """

class ValidatePython(object):    
     def validateCore(self,form,name):
             self.parentClass.validate(self,form)
             new=PythonScript()
             new.__name__=name
             new.source=form.request.POST.get('form.field.source')
             new.arguments=form.request.POST.get('form.field.arguments')
             try:
                result=new.compile()
             except:
                form.submissionError=() 
                if len(new._v_errors) != 0:
                   form.submissionError += new._v_errors + ("Extra Error",) 
                   raise ActionError(new._v_errors) 
             if len(new._v_warnings) != 0:
                   form.submissionError += new._v_warnings + ("Extra Warning",)
                   raise ActinError(new._v_warnings)
             return True
             
class AddPythonAndEdit(ValidatePython,Add):
    parentClass=Add
    def newURL(self,baseURL):
        return baseURL + '/aceedit'

class AddPythonAndTest(ValidatePython,Add):
    parentClass=Add
    def newURL(self,baseURL):
        return self.form.new.testURL

class EditPython (ValidatePython,Edit):
    parentClass=Edit
    def newURL(self,baseURL):
        return baseURL + '/aceedit'

    #Validate on Edit        
    def validate(self,form):
            self.form=form
            name=form.context.__name__
            return self.validateCore(form,name)


    
class EditPythonAndTest(EditPython):
    parentClass=Edit
    def newURL(self,baseURL):
        return self.form.context.testURL        
    
@form_component
@name('addPython')
@context(IBTreeContainer)
@title("Add Python")
@permissions('Manage')
@implementer(IPython)
class AddPythonFunction(AceScripts,AceAddForm):
    subTitle = "Add  a Python  Script (Beta)"
    interface = IPython
    ignoreContent = True
    factory=PythonScript
    
    def postProcess(self):
        self.new.postProcess()

    def footerScripts(self):
        return AceScripts.footerScripts(self)

    def headerScripts(self):
          return AceScripts.headerScripts(self)    
    
    @property
    def actions(self):
        return Actions(
              AddPythonAndEdit(_("Add and Edit","Add -> Edit"), self.factory),
              AddPythonAndTest(_("Add and Test","Add -> Test"), self.factory),
              Cancel(_("Cancel","Cancel")))

    #Validate on Add
    def validate(self,form):
            name=form.request.POST.get('form.field.__name__')
            return self.validateCore(form,name)
    

def make_python_response(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or u'')
        response.content_type=u'application/text'
        return response    

@view_component
@name('index')
@context(IPython)
@title("View")
class Index(View):
    responseFactory = Response
    make_response = make_python_response
        
    def render(self):
               return self.context.source


@form_component
@context(IPython)
@title("AceEit")
@name("aceedit")
@permissions('Manage')
class AceEditPython(AceScripts,AceEditForm):
    subTitle= "Edit a Python Object"
    def footerScripts(self):
        return AceScripts.footerScripts(self)

    def headerScripts(self):
          return AceScripts.headerScripts(self)    

    def postProcess(self):
        self.context.postProcess()
        
    @CachedProperty
    def actions(self):

        action1=EditPython("Save","Save")
        action2=EditPythonAndTest("Save  and View","Save -> View")
        action3=Cancel("Cancel","Cancel")
        return Actions(action1,action2,action3)


