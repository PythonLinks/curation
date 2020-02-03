
#CURRENTLY JUST TO A SINGLE PERSON
#CURRENTLY ONLY USES MAIL QUEUE
from email.message import Message
from zope import schema

from repoze.sendmail.delivery import QueuedMailDelivery, DirectMailDelivery



from zopache.core.viewdecorators import *
from zopache.core import Leaf
from zopache.crud.interfaces import ILeaf
from zopache.pages.interfaces import IRootPage
from zopache.crud.forms import AddNamedForm, EditForm
from zopache.ttw.interfaces import IMailHost
from zopache.core.interfaces import ITreeSecurity
from subprocess import Popen
import os

from here import HERE
dataDir = os.path.join(HERE, 'data')
spoolFile = os.path.join(dataDir, 'spool')
configFile = os.path.join(dataDir, 'qp.config')
runFile = os.path.join(dataDir, 'run2')         
noreply  = '"DO NOT REPLY" <noreply@PythonLinks.info>'
webmaster = '"Christopher Lozinski" <lozinski@PythonLinks.info> '
class Notify (object):

    def notify (self,aFrom,to, subject, content):
        message = Message()
        message['From'] = aFrom
        message['To'] = to
        message['Subject'] = subject
        #text = 'To: ' + to + ' \n'
        #text +='From: ' + from + ' \n'
        message.set_payload(content)
        #mailer = self.parentalAcquire ("MailHost")
        delivery = QueuedMailDelivery(spoolFile)
        to = [to]
        delivery.send(aFrom,to, message)
 
    def sendTheMail(self):
        Popen([runFile ])
           
    def notifyUserNewUser(self):
        subject = "Welcome"
        url = self.url (self.new)
        content = F"""Thank you for signing up. 
                      Here is your user url: {url}"""
        email = '"' + self.new.handle + '" <' + self.new.email + '>'
        self.notify (noreply,email, subject, content)
 
    def notifyAdminsNewUser(self):
        subject = "New User" 
        url = self.url (self.new)       
        content = F"Here is the new user url {url}"
        self.notify (noreply, webmaster, subject, content)       
        self.sendTheMail()
        
    def notifyAdminsNewPage(self):
        #breakpoint()
        subject = "New Page"
        content = self.url (self.new)
        self.notify (noreply,webmaster, subject, content)
        self.sendTheMail()

    def notifyAdminsPageDeleted(self):
        subject = "Page Deleted"
        content = self.request.url
        self.notify (noreply,webmaster, subject, content)        
        self.sendTheMail()
        

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
