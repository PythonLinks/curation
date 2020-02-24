from dolmen.forms.base import Actions
from zopache.crud import actions as formactions
from zopache.ttw.fileaction  import AddFileAction, AddImageAction
from dolmen.container import IBTreeContainer
from zopache.ttw.interfaces import IFile, IImage
from zopache.core.viewdecorators import *
from zopache.crud.forms import AddForm
from zopache.core.uniquename import UniqueName
from zopache.core.interfaces import ITreeSecurity

@form_component
@name('addFile')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddFile(AddForm,UniqueName):
    subTitle='Add a File'
    interface = IFile
    ignoreContent = True

    @property
    def actions(self):
        return Actions(
              AddFileAction("Add File"),   
              formactions.Cancel("Cancel","Cancel"))

@form_component
@name('addImage')
@context(IBTreeContainer)
@title("Add File")
@implementer(ITreeSecurity)
class AddImage(AddFile):
    subTitle='Add an Image'
    interface = IImage
    ignoreContent = True
    @property
    def actions(self):
        return Actions(
              AddImageAction("Add and View"),
              formactions.Cancel("Cancel","Cancel"))
    

