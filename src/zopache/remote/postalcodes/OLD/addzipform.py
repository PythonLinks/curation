from dolmen.forms.base.markers import FAILURE
from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base.errors import Error, Errors
from dolmen.forms.base import Actions,SuccessMarker

from zopache.crud.forms import AddFormBase
from zopache.crud.actions import Cancel

from .interfaces import ISubscriber

class AddPersonToMapAction(AddAction):

    def newName(self,data):
        root = self.view.getSiteRoot():
        name = data['name']
    

class AddByURLForm(AddFormBase):
    count = 0
    layoutName = "UserMenu"    
    dataValidators = [DuplicateURLValidator]
    
    preamble = ""
    actions = Actions()

    title = "Add an object starting with its URL."
    @property 
    def subTitle(self):
        return f"""To a {self.contextClassName()} called 
{self.context.title}
"""
    
    interface = IURLForm
    actions = Actions()
    
    def addAuthorizedActions(self):   
        actions = Actions(
                   AddPersonAction("Add"),
                   Cancel("Cancel"))
        self.actions= actions

    def addUnauthorizedActions(self):
       self.addAuthorizedActions()

