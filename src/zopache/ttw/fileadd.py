

from dolmen.widget.file import FileWidget


from zopache.core.viewdecorators import *
from zopache.crud.forms import AddForm
from dolmen.widget.file import FileSchemaField
from zope.cachedescriptors.property import CachedProperty
from dolmen.forms.base import Actions
from zopache.crud import actions as formactions
from zopache.ttw.fileaction  import AddFileAction, AddImageAction
from dolmen.container import IBTreeContainer
from zopache.ttw.interfaces import IFile, IImage

@form_component
@name('addFile')
@context(IBTreeContainer)
@title("Add File")
@permissions('Manage')
class AddFile(AddForm):
    subTitle='Add a File'
    interface = IFile
    ignoreContent = True

    @CachedProperty
    def actions(self):
        return Actions(
              AddFileAction("Add File","Add File"),   
              formactions.Cancel("Cancel","Cancel"))


@form_component
@name('addImage')
@context(IBTreeContainer)
@title("Add File")
@permissions('Manage')
class AddImage(AddFile):
    subTitle='Add an Image'
    interface = IImage
    ignoreContent = True

    @CachedProperty
    def actions(self):
        return Actions(
              AddImageAction("Add Image","Add Image"),   
              formactions.Cancel("Cancel","Cancel"))    

