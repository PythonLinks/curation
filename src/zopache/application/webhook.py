from slugify import slugify

from zope.interface import Interface
from dolmen.container import IBTreeContainer

from cromlech.security import permissions
from zopache.ttw.container import AdminContainer
from zopache.crud.forms import AddByTitleForm , EditForm
from zopache.core.viewdecorators import *
from zopache.application.interfaces import IAdminContainer
from zopache.crud.interfaces import IZMI

class IWebHook(IBTreeContainer,IZMI):
    title = schema.TextLine(
        title = 'Remote Hook Name',
        description = 'What is the title of this link?',
        required = False,
    )

    webHookURL= schema.URI(
        title = 'Webhook URL',
        description = "The webhook  itself.",
        required = False,
    )    

    serverName = schema.TextLine(
        title = 'Remote Discord Server Name',
        description = 'Which Discord Server?',
        required = True,
    )
    
    serverId = schema.Int(
        title = 'Remote Discord Server Id',
        description = 'Which Discord Server?',
        required = True,
    )
    
    channelName = schema.TextLine(
        title = 'Remote Channel Name',
        description = 'Which Channel?',
        required = True,
    )
    
    channelId = schema.Int(
        title = 'Remote Discord Channel Id',
        description = 'Which Discord Channel?',
        required = False,
    )    

    
@implementer (IWebHook)
class DiscordWebHook(AdminContainer):
    title = ""
    serverName = ""
    channelName = ""
    
    def slug(self):
        return (slugify(self.serverName,lower=True) +
               '-' +
               slugify(self.channelName,lower=True))
    
    @property
    def description(self):
        return self.serverName + " " + self.channelName

    
@form_component
@name('addWebHook')
@context(IAdminContainer)
@permissions('Manage')
class AddWebHook(AddByTitleForm):
    subTitle = 'Add a WebHook'
    interface = IWebHook
    ignoreContent = True
    factory = DiscordWebHook
    def newURL (self,baseURL):
        return "./manage"

#HERE IS THE  EDIT FORM    
@form_component
@context(IWebHook)
@name("edit")
@permissions('Manage')
class EditWebHook(EditForm):
    subTitle='Edit the Web Hook'    
 


