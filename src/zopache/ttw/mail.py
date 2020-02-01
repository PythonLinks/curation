
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
from zopache.core.interfaces import ITreeSecurity
import os




file = os.path.join(HERE, 'qp.config') 
os.spawn ( os.P_NOWAIT, 'qp', file)
           



class Notify (object):
    webmaster  = 'Christopher Lozinski <lozinski@PythonLinks.info>'
    
    def notify (to, subject, content):

        message = Message()
        message['From'] = webmaster
        message['To'] = webmaster
        message['Subject'] = subject
        message.set_payload("content")
        #delivery = QueuedMailDelivery('path/to/queue')
        mailer = self.parentalAcquire ("MailHost")
        delivery = DirectMailDelivery(mailer)
        delivery.send(from, [to], message)

    def notifyUserNewUser(self):
        subject = "Welcome"
        url = view.url (self.new)
        content = """ Thank you for signing up. """
        self.notify (to, subject, content)
 
    def notifyAdminsNewUser(self):
        subject = "New User" 
        url = view.url (self.new)       
        content = F"Here is the new user {url}"
        self.notify (to, subject, content)       

 
    def notifyAdminsNewPage(self):
        subject = "New Page"
        content = view.url (self.new)
        self.notify (to, subject, content)

    def notifyAdminsPageDeleted(self):
        subject = "Page Deleted"
        content = view.request.url
        self.notify (to, subject, content)        
        

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
@implementer(ITreeSecurity)
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
@implementer(ITreeSecurity)
class EditMailHost(EditForm):
    subTitle='Edit the MailHost Object'    
