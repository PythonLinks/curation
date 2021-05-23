from dolmen.forms.base import action, name, context, form_component
from zopache.crud.forms import AddForm, EditForm
from dolmen.forms.base import action, name, context, form_component
from dolmen.forms.base import Actions
from zopache.crud import actions as formactions, i18n as _
from zopache.crud import update as editactions
from zopache.ttw import actions as ttwactions
from zopache.ttw.acescripts import AceScripts
from zopache.crud.forms import TreeSecurityAddForm

class AceAddForm (TreeSecurityAddForm,AceScripts):

    def addAuthorizedActions(self):    
         self.actions = Actions(
              ttwactions.AddAndAceEdit(   "Add -> Ace Edit",
                                        self.factory),
              formactions.AddAndView(
                                       "Add -> View",
                                        self.factory),
              formactions.Cancel("Cancel","Cancel"))


class AddAndSearchForm (AceScripts,AddForm):
    def addAuthorizedActions(self):    
         self.actions = Actions(
              ttwactions.AddAndSearch("Add and Search",
                                          "Add -> Search",
                                        self.factory),
              formactions.Cancel("Cancel","Cancel"))



class AceEditForm(AceScripts,EditForm):
     @property
     def title(self):
         return	"Ace Edit this " + self.className()
     actions = Actions()
            
     def addAuthorizedActions(self):
              self.actions =  Actions(
              ttwactions.SaveAndAceEdit(_("Save","Save")),
              editactions.SaveAndView(_("Save and View","Save -> View")),
              formactions.Cancel(_("Cancel","Cancel")))


class PugEditForm(AceScripts,EditForm):
    aceMode = "jade"
    def update(self):
         if self.treeSecurity():
           self.actions = Actions(
              ttwactions.SaveAndAceEdit(_("Save","Save")),
              editactions.SaveAndView(_("Save and View","Save -> View")),
              editactions.SaveAndViewJS(_("Save -> JS","Save -> JS")),
              #formactions.SaveAndViewHTML(_("Save -> HTML","Save -> HTML")),
                      formactions.Cancel(_("Cancel","Cancel")))    


    
