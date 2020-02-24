#Copyright Christopher Lozinski.  All rights reserved.
from zope.interface import implementer

from dolmen.forms.base import Actions

from zopache.core.viewdecorators import *
from zopache.crud.actions import Cancel
from zopache.crud.actions import AddByTitle, Edit
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from cromlech.webob.response import Response
from dolmen.view import  make_view_response
from dolmen.container import IBTreeContainer

from zopache.crud import actions as formactions, i18n as _
from zopache.ttw.acescripts import AceScripts
from zopache.crud.forms import AddForm
from zopache.pages.notebook import Notebook
from zopache.pages.interfaces import INotebook,IPage
from zopache.core import View
from zopache.core.page  import  Page
from zopache.pages.notebook import Notebook
from zopache.pages.interfaces import INotebook, IAddNotebook
from zopache.core.interfaces import ITreeSecurity

class  AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/json");
        </script>
        """

class AddAndEdit(AddByTitle):
    parentClass=AddByTitle
    def newURL(self,baseURL):
        return baseURL + '/aceedit'

class AddAndView(AddByTitle):
    parentClass=AddByTitle
    def newURL(self,baseURL):
        return baseURL 

class Edit (Edit):
    parentClass=Edit
    def newURL(self,baseURL):
        return baseURL + '/aceedit'


from zopache.crud.forms import AddByTitleForm
@form_component
@name('addNotebook')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddNotebook(AddByTitleForm):
    subTitle='Upload a Notebook'
    interface = IAddNotebook
    ignoreContent = True
    factory = Notebook
    
    @property
    def actions(self):
        return Actions(
              AddAndEdit(_("Add and Edit","Add -> Edit"), self.factory),
              #AddAndView(_("Add and View","Add -> View"), self.factory),
              formactions.Cancel("Cancel","Cancel"))
    
    

#THIS ONE WAS LIKE JSON FORM.     
"""
@view_component
@name('addNotebook2')
@context(IPage)
@target(IView)
@permissions('Manage')
class AddNotebook2(AceScripts,AddByTitleForm):
    subTitle = "Add a Read-Only Jupyter Notebook"
    interface = INotebook
    ignoreContent = True
    factory=Notebook
    
    def footerScripts(self):
        return AceScripts.footerScripts(self)

    def headerScripts(self):
          return AceScripts.headerScripts(self)    
    
    @property
    def actions(self):
        return Actions(
              AddAndEdit(_("Add and Edit","Add -> Edit"), self.factory),
              AddAndView(_("Add and View","Add -> View"), self.factory),
              Cancel(_("Cancel","Cancel")))
"""

@view_component
@name('index')
@context(INotebook)
class Index(Page):
    responseFactory = Response

    ake_response = make_view_response
        
    def render(self):
        return self.context['inde.html'].getSource()

from zopache.crud.forms import EditDemoForm
@form_component
@context(INotebook)
@name("acedemo")
class AceDemo(AceScripts,EditDemoForm):
    subTitle= "Demo of Ace Editing a Jupyter Notebook.  Saving is disabled."
    
           
@form_component
@context(INotebook)
@name("aceedit")
@implementer(ITreeSecurity)         
class AceEdit(AceScripts,AceEditForm):
    subTitle= "Edit a Notebook"

    @property
    def actions(self):
        action1=Edit("Save","Save")
        #action2=EditAndView("Save  and View","Save -> View")
        action3=Cancel("Cancel","Cancel")
        return Actions(action1,action3)

    def postProcess(self, view = None):
        self.context.postEditProcess(self)

