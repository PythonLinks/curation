from dolmen.forms.base import Actions
from zopache.crud import actions as formactions
from zopache.ttw.fileaction  import(
    AddFileAction,
    AddImageAction,
    AddSocialMediaImageAction,
    AddLogoAction,
    AddBannerAction)    

from dolmen.container import IBTreeContainer
from zopache.ttw.interfaces import IFile, IAddBTreeImage
from zopache.core.viewdecorators import *
from zopache.crud.forms import AddForm
from zopache.core.uniquename import UniqueName
from zopache.core.interfaces import ITreeSecurity
from zopache.forms.imagevalidator import BannerValidator, LogoValidator


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
@implementer(ITreeSecurity)
class AddImage(AddFile):
    subTitle='Add an Image'
    interface = IAddBTreeImage
    ignoreContent = True
    @property
    def actions(self):
        return Actions(
              AddImageAction("Add and View"),
              formactions.Cancel("Cancel","Cancel"))
    
#ADD A BANNER IMAGE
@form_component
@name('addBanner')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddBanner(AddImage):
    dataValidators = [BannerValidator]     
    subTitle='Add a Banner'
    @property
    def fields(self):
        return  Fields(self.interface)
    
    @property
    def actions(self):
        return Actions(
              AddBannerAction("Add and View"),
              formactions.Cancel("Cancel","Cancel"))
    

#ADD A LOGO IMAGE
@form_component
@name('addLogo')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddLogo(AddImage):
    dataValidators = [LogoValidator] 
    subTitle="Add a Logo or politician's photo."
    @property
    def fields(self):
        return  Fields(self.interface)
    
    @property
    def actions(self):
        return Actions(
              AddLogoAction("Add and View"),
              formactions.Cancel("Cancel","Cancel"))


    #ADD A SOCIAL MEDIA  IMAGE
@form_component
@name('addSocialMediaImage')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddSocialMediaImage(AddImage):
    dataValidators = [LogoValidator] 
    subTitle="Add a Social Media Image."
    @property
    def fields(self):
        return  Fields(self.interface)
    
    @property
    def actions(self):
        return Actions(
              AddSocialMediaImageAction("Add and View"),
              formactions.Cancel("Cancel","Cancel"))


