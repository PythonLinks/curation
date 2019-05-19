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
from RestrictedPython import safe_builtins, utility_builtins, limited_builtins
from RestrictedPython import RestrictingNodeTransformer
from .interfaces import ITestURL
from zopache.ttw.interfaces import IPython
from zopache.core import getRoot
from zopache.core.breadcrumbs import parents

import RestrictedPython
from RestrictedPython import _compat
from dolmen.forms.base.interfaces import ActionError



@implementer(IPython)
class PythonScript(Leaf):
    icon="ttwicons/Python.svg"
    
class  AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/python");
        </script>
        """

class AddPythonAndEdit(Add):
    parentClass=Add
    def newURL(self,baseURL):
        return baseURL + '/aceedit'

class AddPythonAndTest(Add):
    parentClass=Add
    def newURL(self,baseURL):
        return self.form.new.testURL

class EditPython (Edit):
    parentClass=Edit
    def newURL(self,baseURL):
        return baseURL + '/aceedit'

    
class EditPythonAndTest(EditPython):
    parentClass=Edit
    def newURL(self,baseURL):
        return self.form.context.testURL        
    
@form_component
@name('addPython')
@context(IBTreeContainer)
#@target(ITab)
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
              #AddPythonAndTest(_("Add and Test","Add -> Test"), self.factory),
              Cancel(_("Cancel","Cancel")))

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


