from dolmen.container import IBTreeContainer


from zopache.crud.forms import AddByNameForm , EditForm
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import IPageBase
from zopache.core.interfaces import ITreeSecurity
from zopache.remote.mastodon.interfaces import IServer
from zopache.remote.mastodon.server import Server

@form_component
@name('addServer')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddMastodonServer(AddByNameForm):
    subTitle='Add a Mastodon Host'
    interface = IServer
    ignoreContent = True
    factory=Server
    
    def newURL(self,baseURL):
        return baseURL + "/edit"

    #HERE IS THE  EDIT FORM
@form_component
@context(IServer)
@name("edit")
@implementer(ITreeSecurity)
class EditServer(EditForm):
    subTitle='Edit the Mastodon Server'    
    interface = IServer 

