#Copyright Christopher Lozinski.  All rights reserved.
from zope.interface import implementer

from dolmen.forms.base import Actions

from zopache.core.viewdecorators import *
from zopache.crud.actions import Cancel
from zopache.crud.actions import Add
from zopache.crud.update import Edit
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from cromlech.webob.response import Response
from dolmen.view import  make_view_response

from zopache.crud import actions as formactions, i18n as _
from zopache.ttw.acescripts import AceScripts
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.pages.markdown import Markdown
from zopache.pages.interfaces import IMarkdown, IPage
from zopache.core import View
from zopache.ttw.mail import Notify
from zopache.core.interfaces import ITreeSecurity

class  AceScripts(AceScripts):
    aceMode = 'markdown'

class AddAndEdit(Add):
    parentClass=Add
    def newURL(self,baseURL):
        return baseURL + '/aceedit'

class AddAndView(Add):
    parentClass=Add
    def newURL(self,baseURL):
        return baseURL 

class Edit (Edit):
    parentClass=Edit
    def newURL(self,baseURL):
        return baseURL + '/aceedit'
    
class EditAndView (Edit):
    parentClass=Edit
    def newURL(self,baseURL):
        return baseURL    
    
@form_component
@name('addMarkdown')
@context(IPage)
@implementer(ITreeSecurity)
class AddMarkdown(AceScripts,AceAddForm, Notify):
    subTitle = "Add a Markdown Page"
    interface = IMarkdown
    ignoreContent = True
    factory=Markdown
    def __init__(self):
        Notify.__init__(self)
        AceScripts.__init__(self)
        AceAddForm.__init__(self)
    
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

@view_component
@name('index')
@context(IMarkdown)
@title("View")
class Index(View):
    responseFactory = Response
    make_response = make_view_response
        
    def render(self):
               return self.context._html

           
from zopache.crud.forms import EditDemoForm
@form_component
@context(IMarkdown)
@name("acedemo")
class AceDemo(AceScripts,EditDemoForm):
    subTitle= "Demo of Ace Editing Markdown objects.  Saving is disabled."      
           
@form_component
@context(IMarkdown)
@name("aceedit")
@implementer(ITreeSecurity)
class AceEdit(AceScripts,AceEditForm):
    subTitle= "Edit a Markdown Page"

    #@property
    #def actions(self):
    #    action1=Edit("Save","Save")
    #    action2=EditAndView("Save  and View","Save -> View")
    #    action3=Cancel("Cancel","Cancel")
    #    return Actions(action1,action2,action3)



