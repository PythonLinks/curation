#Copyright Christopher Lozinski.  All rights reserved.
import os
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
from zopache.crud.update import Edit
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from dolmen.view import name, context, view_component
from dolmen.view import View
from cromlech.webob.response import Response
from dolmen.view import View, make_view_response
from zopache.crud import actions as formactions, i18n as _
from zopache.crud import update  as editactions

import RestrictedPython
from RestrictedPython import _compat
from RestrictedPython import compile_restricted_function
from RestrictedPython import compile_restricted
from RestrictedPython import RestrictingNodeTransformer
from RestrictedPython import safe_builtins, utility_builtins, limited_builtins


from zopache.core import Leaf
from zopache.python.acescripts import AceScripts
from zopache.python.interfaces import IPython
from zopache.ttw.addeditforms import AceEditForm
from   zopache.python.mixed import ObjectFile
from zopache.python.mixed import ObjectFile
from zopache.python.interfaces import IPythonFolder, IPythonIndex
from zopache.ttw.javascript import SourceBase
from zopache.python.filesystem import Directory

@implementer(IPython)
class Python(Leaf,SourceBase,ObjectFile):
    def __init__(self):
        Leaf.__init__(self)
    icon="ttwicons/Python.svg"
        
    def getJavascriptSource(self):
        javascriptObject = self.javascriptObject()
        if javascriptObject:
           return javascriptObject.source
        else:
           base = "WARNING Not able to access: " 
           return base + self.javascriptFolder().fileName + self.javascriptFileName()


    def javascriptFileName(self):
        return self.getJavascriptFileName(self.__name__)
    
    def getJavascriptFileName(self,name):
        return self.__name__[:-3] + '.js'
        
    def javascriptFolder(self):
        parent = self.__parent__
        path = self.javascriptFolderPath()
        if not os.path.exists(path):
            os.makedirs(path)
        return parent["__target__"]
       
    def javascriptFolderPath(self):
        parent = self.__parent__
        path = os.path.join (parent.path,'__target__') 
        return path           

    def outputPath(self):
        jsPath =  self.javascriptFolder().path
        path = os.path.join(jsPath, "output")
        return path
    
    def javascriptObject(self):    
        javascriptFolder = self.javascriptFolder()
        javascriptFileName = self.javascriptFileName()
        if javascriptFolder.exists(javascriptFileName):
            return javascriptFolder[javascriptFileName]
        else:
            return None
    
    def compile(self,view):
        cmd = 'transcrypt ' +  self.path +  " > " + self.outputPath()
        os.system(cmd)

    def deleteJavascriptObject(self,view):
        try:
            self.javascriptObject().delete(view) 
        except:
            pass

    def postAddProcess (self,view):
       if IPythonFolder.providedBy (self.__parent__): 
           self.exportSource(self.source)
           self.compile()

    def postEditProcess(self,view = None):
       if IPythonFolder.providedBy (self.__parent__):
           self.exportSource()
           self.compile(view)
        
    def preMoveProcess(self,view):
       if IPythonFolder.providedBy (self.__parent__):
           self.deleteJavascriptObject(view)
           self.delete(view)
           self.setLastPath()

    # BUG IF MOVING BETWEEN REGULAR FOLDER AND TRANSCRYPT FOLDER       
    def postMoveProcess(self,view):    
       if IPythonFolder.providedBy (self.__parent__):
           self.exportSource()
           self.compile(view)

    def preDeleteProcess(self,view):
       if IPythonFolder.providedBy (self.__parent__):
           self.delete(view)
           self.deleteJavascriptObject(view)    

class EditPython (Edit):
    parentClass=Edit
    def newURL(self,baseURL):
        return baseURL + '/aceedit'

    
class EditPythonAndTest(EditPython):
    parentClass=Edit
    def newURL(self,baseURL):
        return self.form.context.testURL        

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
class AceEditPython(AceEditForm):
    subTitle= "Edit a Python Object"

    @property
    def actions(self):
        action1=EditPython("Save","Save")
        action2=EditPythonAndTest("Save  and View","Save -> View")
        action3=Cancel("Cancel","Cancel")
        return Actions(action1,action2,action3)

    def postProcess(self):

        self.context.postEditProcess(self)


