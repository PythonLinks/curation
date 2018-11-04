

from dolmen.widget.file import FileWidget


from zopache.core.viewdecorators import *
from zopache.crud.forms import AddForm
from dolmen.widget.file import FileSchemaField
from zope.cachedescriptors.property import CachedProperty
from dolmen.forms.base import Actions
from zopache.crud import actions as formactions
from zopache.ttw.fileaction  import AddFileAction
from dolmen.container import IBTreeContainer
from zopache.ttw.interfaces import IFile

@form_component
@name('addFile')
@context(IBTreeContainer)
#@target(ITab)
@title("Add File")
@permissions('Manage')
class AddFile(AddForm):
    subTitle='Add a File'
    interface = IFile
    ignoreContent = True


#    def updateWidgets(self):
#        self.fieldWidgets.extend(self.fields)
#        self.fieldWidgets = self.fieldWidgets.select('form.field.__name__')
#        new = FileWidget( self.fields['data'],self,self.request)
#        self.fieldWidgets.append(new)
#        
#        self.actionWidgets.extend(self.actions)#

#        self.fieldWidgets.update()
#        self.actionWidgets.update()        


    @CachedProperty
    def actions(self):
        return Actions(
              AddFileAction("Add File","Add File"),   
              formactions.Cancel("Cancel","Cancel"))

