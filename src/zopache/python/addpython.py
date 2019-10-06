from zope.interface import Interface
from zope.schema import TextLine

from dolmen.forms.base import Actions

from zopache.ttw.addeditforms import AceAddForm
from zopache.ttw.acescripts import AceScripts
from zopache.core.viewdecorators import *
from zopache.python.python import Python
from zopache.python.interfaces import IPython, IPythonFolder
from zopache.crud.actions import Add
from zopache.crud import actions as formactions, i18n as _
from zopache.crud.actions import Cancel
from zopache.python.python import AceScripts

class PyLine (TextLine):
    def validate (self,value):
        if ((len(value) <3) or
           (value [-3:] != '.py')
            ):
           raise ValueError( value, ": Python File Names must end in .py,")
            
        return TextLine.validate(self,value)    

class IName(Interface):
      __name__ = PyLine(
           title=(u"URL Segment Name (required)"),
           description = "Will be made web-safe.", 
           required=True,
           default=None)


      
class AddPythonAndEdit(Add):
    parentClass=Add
    def newURL(self,baseURL):
        return baseURL + '/aceedit'

class AddPythonAndTest(Add):
    parentClass=Add
    def newURL(self,baseURL):
        return self.form.new.testURL

    
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

    @property
    def fields(self):
        return  Fields(IName,self.interface)    
