
#CURRENTLY JUST TO A SINGLE PERSON
#CURRENTLY ONLY USES MAIL QUEUE

from zope import schema

from repoze.sendmail.delivery import QueuedMailDelivery, DirectMailDelivery

from here import HERE

from zopache.core.viewdecorators import *
from zopache.core import Leaf
from zopache.crud.interfaces import ILeaf
from zopache.pages.interfaces import IRootPage
from zopache.crud.forms import AddNamedForm, EditForm
from zopache.ttw.interfaces import IMailHost


    

@implementer (IMailHost)
class MailHost(Leaf):
    def __init__(self):
        Leaf.__init__(self)

    def getMailSpoolPath(self):
        path = os.path.join(HERE,'data')
        path = os.path.join(path,'mail')
        path = os.path.join(path,'mailspool')        
        return path
        
    #def sendDirect(from, to, message):

    def sendQueued(message):        
        delivery = QueuedMailDelivery(self.getMailSpoolPath())
        delivery.send (message['From'], [message['To']], message)
    
@form_component
@name('addMailHost')
@context(IRootPage)
@permissions('Manage')
class AddMailHost(AddNamedForm):
    subTitle='Add a MailHost'
    interface = IMailHost
    ignoreContent = True
    factory=MailHost
    def newName(self,data):
        return "MailHost"
    
#HERE IS THE  EDIT FORM
@form_component
@context(IMailHost)
@name("edit")
@permissions('Manage')
class EditMailHost(EditForm):
    subTitle='Edit the MailHost Object'    
