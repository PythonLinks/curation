from zopache.core.viewdecorators import *
import crom
from zopache.crud.forms import  EditForm
from zope.cachedescriptors.property import CachedProperty
from dolmen.forms.base import Actions
from cromdemo.interfaces import ITab
@form_component
@context(Interface)
@crom.target(ITab)
@title("Edit Permissions")
@name("permissions2")
@permissions('Manage')
class EditPermissions(EditForm):
    @CachedProperty
    def actions(self):
        return Actions(formactions.SaveAndView("Save  and View",
                                               "Save -> View"))
	      
