from cromlech.file import FileField
from dolmen.container import IBTreeContainer
from dolmen.forms.base import Actions

from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.crud.actions import Cancel
from zopache.forms.restoreactions  import RestoreAction, ReplaceAction

class IRestore(Interface):
         data = FileField(title=u'Choose the Backup File to be restored.')

@form_component
@name('restore')
@context(IBTreeContainer)
@title("Restore a Branch")
@permissions('Manage')
class Restore(Form):
    title = "Restore From Backups"
    subTitle="Replace a Branch or Create a New Branch"
    interface = IRestore
    ignoreContent = True
    
    @property
    def fields(self):
        return  Fields(IRestore)

    @property
    def actions(self):
        return Actions(
              RestoreAction("Restore Branch"),
              ReplaceAction("Replace This Branch"),
              Cancel("Cancel","Cancel"))




