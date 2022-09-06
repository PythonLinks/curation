from dolmen.forms.base import Actions

from zope import interface
from zope import schema
from zope.schema.interfaces import IField
from zope.interface import Interface

from dolmen.container import IBTreeContainer

from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.crud.forms import EditDemoForm
from zopache.core.getroot import getProducts
from zopache.core.viewdecorators import *
from zopache.core import Leaf
from zopache.ttw.acescripts import AceScripts as AceScriptsBase
from zopache.core.interfaces import ITreeSecurity
from zopache.python.interfaces import IPyodide
from zopache.crud import update as editActions                    
from zopache.python.interfaces import IPython

@implementer(IPyodide)      
class  Pyodide (Leaf):
    icon="ttwicons/Python.svg"    
    source ="\n\n\n"
    title=u''

class  AceScripts(AceScriptsBase):
    aceMode = 'python'
    actions = Actions()
    
    def update(self):
        pyodide = self.getTemplates()["Pyodide"]
        pug = pyodide["template"]
        self.template = pug.setTemplate()
        
    def  footerScripts(self):
        return ""

    
@form_component
@context(IPyodide)
@target(IView)
@name("aceedit")
class AceEdit(AceScripts,AceEditForm):
    title = "cPython Editor and REPL"
    subTitle = "It is a syntax-checking editor."
    def newURL():
        return "edit"
    
    def update(self):
        AceScripts.update(self)
        AceEditForm.update(self)

@form_component
@context(IPyodide)
@target(IView)
@name("index")
class Index (AceEdit):
    pass
        
@form_component
@name('addPyodide')
@context(IBTreeContainer)
@implementer(IPython)
@implementer(ITreeSecurity)
class AddPython(AceAddForm):
    aceMode = "python"
    subTitle = "Add a cPython (Pyodide) Object"
    interface = IPyodide
    ignoreContent = True
    factory=Pyodide
    
