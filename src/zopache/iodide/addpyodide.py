from cromlech.webob.response import Response
from dolmen.view import  make_view_response
from zopache.core import View

from dolmen.forms.base import Actions
from zopache.pages.pageactions import *
from zopache.crud import actions as formactions
from zopache.pages.pageactions import *
from zopache.core.viewdecorators import *
from zopache.ttw.html import CkScripts
from zopache.ttw.html import AddCkHTMLBase
from zopache.ttw.acescripts import AceScripts
from zopache.pages.interfaces import IPage

from zopache.core.uniquename import UniqueName
from zopache.crud.forms import AddByTitleForm
from zopache.iodide.iodide import Iodide
from zopache.iodide.interfaces import IIodide
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.core.interfaces import ITreeSecurity

class AddPageBase(AddCkHTMLBase,AddByTitleForm,UniqueName):

    def getSubTitle(self):
        return (
                "To a " +  
                self.context.webClass +
                u' called: ' +
                self.context.getTitle()
               )

    @property
    def actions(self):
        return Actions(
              AddAndView("Add and View", self.factory),
              AddAndAceEdit("Add and AceEdit", self.factory),
              formactions.Cancel("Cancel","Cancel"))



class  AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/text");
        </script>
        """
    
#HERE IS THE ACE EDIT FORM
@form_component
@context(IIodide)
@title("AceEdit")
@name("aceedit")
@implementer(ITreeSecurity)
class AceEditIodide(AceScripts,AceEditForm):
    subTitle='Edit an Iodide Object'

    
@view_component
@name('addIodide')
@title("Add Iodide")
@target(IView)
@context(IPage)    
@implementer(ITreeSecurity)
class AddIodide(AceScripts,AddPageBase):
    interface = IIodide
    label="Add an Iodide Object"
    subTitle='Add an Iodide Object'    
    factory = Iodide


    
