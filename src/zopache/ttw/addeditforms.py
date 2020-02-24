from dolmen.forms.base import action, name, context, form_component
from zopache.crud.forms import AddForm, EditForm
from dolmen.forms.base import action, name, context, form_component
from dolmen.forms.base import Actions
from zopache.crud import actions as formactions, i18n as _
from zopache.ttw import actions as ttwactions


class AceAddForm (AddForm):
    @property
    def actions(self):
        return Actions(
              ttwactions.AddAndAceEdit(_("Add and Ace Edit",
                                          "Add -> Ace Edit"),
                                        self.factory),
              formactions.AddAndView(_("Add  and View",
                                       "Add  -> View"),
                                        self.factory),
              formactions.Cancel(_("Cancel","Cancel")))


class AddAndSearchForm (AddForm):
    @property
    def actions(self):
        return Actions(
              ttwactions.AddAndSearch(_("Add and Search",
                                          "Add -> Search"),
                                        self.factory),
              formactions.Cancel(_("Cancel","Cancel")))



class AceEditForm(EditForm):
    @property
    def actions(self):
        return Actions(
              ttwactions.SaveAndAceEdit(_("Save","Save")),
              formactions.SaveAndView(_("Save  and View","Save -> View")),
              formactions.SaveAndTest(_("Save  and Test","Save -> Test")),     
              formactions.Cancel(_("Cancel","Cancel")))


class PugEditForm(EditForm):
    @property
    def actions(self):
        return Actions(
              ttwactions.SaveAndAceEdit(_("Save","Save")),
            #  formactions.SaveAndView(_("Save  and View","Save -> View")),
            #  formactions.SaveAndViewJS(_("Save -> JS","Save -> JS")),
              #formactions.SaveAndViewHTML(_("Save -> HTML","Save -> HTML")),
              #formactions.SaveAndTest(_("Save  and Test","Save -> Test")), 
              formactions.Cancel(_("Cancel","Cancel")))    


    
