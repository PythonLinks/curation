from zopache.crud.forms import AddByNameForm , EditForm
from zopache.core.viewdecorators import *
from zopache.ttw.mail import MailHost
from zopache.pages.interfaces import IPage
from zopache.core.interfaces import ITreeSecurity
from zopache.ttw.interfaces import IMailHost

@form_component
@name('addMailHost')
@context(IPage)
@implementer(ITreeSecurity)
class AddMailHost(AddByNameForm):
    subTitle='Add a MailHost'
    interface = IMailHost
    ignoreContent = True
    factory=MailHost
    def newName(self,data):
        return "MailHost"
    def newURL (self,baseURL):
        return "./manage"

    #HERE IS THE  EDIT FORM
@form_component
@context(IMailHost)
@name("aceedit")
@implementer(ITreeSecurity)
class EditMailHost(EditForm):
    subTitle='Edit the MailHost Object'    
 
    """    
    def sendOneNewsletter(self):
        to = self.mailer.postMaster
        articles = self.context.bestMostRecentPage()
        self.createOneNewsLetter(to, self.sender, articles)
        self.sendTheMail()
    """

@form_component
@context(IMailHost)
@name("index")
@implementer(ITreeSecurity)
class EditMailHost(EditForm):
    def render(self):
        return "This is a Mail Host object."
