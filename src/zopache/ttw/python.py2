#sheThis software is subject to the CV License Agreement
from zope.schema import ValidationError
from dolmen.forms.base import Actions
from zopache.crud   import i18n as _
from zopache.crud.actions import Cancel
from . import actions  as ttwactions
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
from zopache.application.interfaces import ITab
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
from zopache.ttw.acescripts import AceScripts
from zopache.ttw.interfaces import ISourceLeaf
from RestrictedPython import safe_builtins, utility_builtins, limited_builtins
from RestrictedPython import RestrictingNodeTransformer
from .interfaces import ITestURL

class OwnRestrictingNodeTransformer(RestrictingNodeTransformer):
        pass

policy = OwnRestrictingNodeTransformer

policy_instance = OwnRestrictingNodeTransformer(
            errors=[],
            warnings=[],
            used_names=[]
        )


class IPython(ISourceLeaf,ITestURL):
    """Basic Python  FORM with CRUD"""
    arguments = schema.TextLine(
        title = u'Arguments',
        description = u'An optional comma separated list of arguments',
        default='',
        required = False,
    )    
    
    source= schema.Text(
        title = u'Python Source Code',
        description = u'The Python code goes here.',
        required = False,
        default = u'',
    )
    title = schema.TextLine(
        title = u'Title',
        description = u'A short reminder of what this Python code  does or its version name.',
        default='',            
        required = False,
    )



@implementer(IPython)
class PythonScript(Leaf):
    icon="ttwicons/Python.svg"    
    def commands(self,view):
        url=view.url(self)
        index=view.liHref(url+'/index','View')
        manual=view.liHref('http://www.zopache.com/baseicwebobjects/css','CSS Manual')
        return index + manual 

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
            self.__name__)
        self._v_code=compiled.code
        self._v_errors=compiled.errors
        self._v_warnings=compiled.warnings
        #Not yet needed, but someone may want the following
        #self._v_used_names=compiled.used_names
        safe_locals = {}
        #safe_globals = (safe_builtins +
        #                limited_builtins +
        #                utility_builtins)
        
        exec(compiled.code, safe_builtins, safe_locals)
        self._v_compiledFunction = safe_locals[self.__name__]
    
    def __call__(self,*args, **kwargs):
        code=self.getCode()
        #Apparently templates always add **kwargs
        numberOfArguments=len(args)
        if (numberOfArguments ==1):
                return code()
        else:
                return code(args)


class  AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/python");
        </script>
        """

class ValidatePython(object):    
     def validateCore(self,form,name):
             self.parentClass.validate(self,form)
             new=Pythonscript()
             new.__name__=name
             new.source=form.request.POST.get('form.field.source')
             new.arguments=form.request.POST.get('form.field.arguments')
             result=new.compile()
             if len(new._v_errors) != 0:
                 self.errors="Failed"
                 raise ValidationError()
             if len(new._v_warnings) != 0:
                 self.errors="Failed"
                 raise ValidationError()             
             return True
             
class AddPythonAndEdit(ValidatePython,Add):
    parentClass=Add
    def newURL(self,baseURL):
        return baseURL + '/ckedit'

class AddPythonAndTest(ValidatePython,Add):
    parentClass=Add
    def newURL(self,baseURL):
        return self.form.new.testURL

class EditPython (Edit):
    parentClass=Edit
    def newURL(self,baseURL):
        return baseURL + '/ckedit'

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
@name('addPythonFunction')
@context(IBTreeContainer)
#@target(ITab)
@title("Add Python")
@permissions('Manage')
@implementer(IWeb)
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
    
    def commands(self):
        manual=self.liHref('http://www.zopache.com/baseicwebobjects/css','CSS Manual')
        return manual 
    @CachedProperty
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
@target(ITab)
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


