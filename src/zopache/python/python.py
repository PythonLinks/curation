#Copyright Christopher Lozinski.  All rights reserved.
import subprocess

from zope.schema import ValidationError
from zope.interface import implementer

from dolmen.forms.base import Actions
from dolmen.container import IBTreeContainer
from crom import target, order
from dolmen.forms.base import action, name, context, form_component
from cromlech.browser.directives import title
from cromlech.security import permissions
from dolmen.forms.base.interfaces import ActionError

from zopache.crud.actions import Cancel
from zopache.ttw import actions  as ttwactions
from zopache.crud.actions import Add,Edit
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from dolmen.view import name, context, view_component
from dolmen.view import View
from cromlech.webob.response import Response
from dolmen.view import View, make_view_response
from zopache.crud import actions as formactions, i18n as _

import RestrictedPython
from RestrictedPython import _compat
from RestrictedPython import compile_restricted_function
from RestrictedPython import compile_restricted
from RestrictedPython import RestrictingNodeTransformer
from RestrictedPython import safe_builtins, utility_builtins, limited_builtins


from zopache.core import Leaf
from zopache.ttw.acescripts import AceScripts
from zopache.python.interfaces import IPython
from zopache.python.filesystem import FileBase
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from   zopache.python.folder import MixedObject
from zopache.python.interfaces import IPythonFolder, IPythonIndex
from zopache.ttw.javascript import SourceBase

@implementer(IPython)
class Python(SourceBase,Leaf,MixedObject,FileBase):
    def __init__(self):
        Leaf.__init__(self)
    icon="ttwicons/Python.svg"

    def getJavascriptSource(self):
        javaScriptObject = self.javascriptObject()
        if javascriptObject:
           return javascriptObject.source
        else:
           base = "WARNING Not able to access: " 
           return base + javascriptFoler.fileName + self.javascriptFileName()


    def javascriptFileName(self):
        return self.getJavascriptFileName(self.__name__)
    
    def getJavascriptFileName(self,name):
        return self.__name__[:-3] + '.js'
        
      
    def javascriptObject(self):    
        javascriptFolder = self.__parent__["__javascript__"]
        javascriptFileName = self.javascriptFileName()
        if javascriptFolder.exists(javascriptFileName):
            return javascriptFolder[javascriptName]
        else:
            return None
    
    def compile(self,view):
        result = subprocess.run( ['transcrypt', self.path])
        self.displayResult(result,view)
                                 
    def deleteJavascriptObject(self,view):
        self.javascriptObject.delete(view)

    def preDeleteProcess(self,view):
        self.delete(view)
        self.deleteJavascriptObject(view)
        
    def postEditProcess(self,view):
        self.exportSource(self.source)
        self.compile()
        
    def postAddProcess (self,view):
        FileBase.__init__(self)        
        self.exportSource(self.source)
        self.compile(view)
        self.setLastPath()

    def preMoveProcess(self,view):
        self.deleteJavascriptObject(view)
        self.delete(view)
        
    def postMoveProcess(self,view):    
        self.exportSource()
        self.compile(view)
        self.setLastPath()

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
@context(IPythonFolder)
@title("Add Python")
@permissions('Manage')
@implementer(IPython)
class AddPython(AceScripts,AceAddForm):
    subTitle = "Add  a Python Object"
    interface = IPython
    ignoreContent = True
    factory=Python
    
    def footerScripts(self):
        return AceScripts.footerScripts(self)

    def headerScripts(self):
          return AceScripts.headerScripts(self)    
    
    @property
    def actions(self):
        return Actions(
              AddPythonAndEdit(_("Add and Edit","Add -> Edit"), self.factory),
              #AddPythonAndTest(("Add and Test","Add -> Test"), self.factory),
              Cancel(_("Cancel","Cancel")))

def make_python_response(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or u'')
        response.content_type=u'application/text'
        return response    

@view_component
@name('index')
@context(IPythonIndex)
@title("View")
class Index(View):
    responseFactory = Response
    make_response = make_python_response
        
    def render(self):
               return self.context.source



           
from zopache.crud.forms import EditDemoForm
@form_component
@context(IPython)
@name("acedemo")
class AceDemo(AceScripts,EditDemoForm):
    subTitle= "Demo of Ace Editing Python objects.  Saving is disabled."      
           
@form_component
@context(IPython)
@name("aceedit")
@permissions('Manage')
class AceEditPython(AceScripts,AceEditForm):
    subTitle= "Edit a Python Object"

    @property
    def actions(self):

        action1=EditPython("Save","Save")
        action2=EditPythonAndTest("Save  and View","Save -> View")
        action3=Cancel("Cancel","Cancel")
        return Actions(action1,action2,action3)


