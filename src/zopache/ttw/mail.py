
#CURRENTLY JUST TO A SINGLE PERSON
#CURRENTLY ONLY USES MAIL QUEUE
from email.message import Message
from subprocess import Popen

from zope import schema
from repoze.sendmail.delivery import QueuedMailDelivery
from z3c.schema.email  import RFC822MailAddress as Email

from zopache.core.viewdecorators import *
from zopache.core import Leaf
from zopache.crud.interfaces import ILeaf
from zopache.pages.interfaces import IPage
from zopache.crud.forms import AddNamedForm, EditForm
from zopache.core.interfaces import ITreeSecurity
from zopache.ttw.interfaces import IMailHost
 
import os

from dolmen.message.utils import send

from here import HERE
dataDir = os.path.join(HERE, 'data')
class Notify (object):

    def notify (self,aFrom,to, subject, content):
        mailer = self.mailer
        if mailer == None:
           return         
        message = Message()
        message['From'] = aFrom
        message['To'] = to
        if self.isAuthenticated():
           replyTo = self.request.principal.email
           if replyTo != to:
              message['Reply-To'] = replyTo
        message['Subject'] = subject
        #text = 'To: ' + to + ' \n'
        #text +='From: ' + from + ' \n'
        message.set_payload(content)
        delivery = QueuedMailDelivery(self.spoolFile())
        to = [to]
        delivery.send(aFrom,to, message)
        
    def spoolFile(self):
        mailer = self.mailer
        if mailer == None:
           return
        parentName = mailer.__parent__.__name__
        spoolFolder = os.path.join(dataDir, 'spool')
        spoolFile = os.path.join(spoolFolder, parentName)        
        return spoolFile
    
    def sendTheMail(self):
        mailer = self.mailer
        if mailer == None:
           return 
        command = ['qp',
                   '--force-tls',
                   '--hostname', mailer.smtpServer,
                   '--port',     str(mailer.port), 
                   '--username', mailer.userName, 
                   '--password', mailer.password]
        if (mailer.debug):
           command.append('--debug-smtp')            
        command.append(self.spoolFile())
        print (' '.join (command))
        Popen(command)
     
    
        
    def notifyUserNewUser(self):
        self.mailer = mailer = self.parentalAcquire ("MailHost")
        if mailer == None:
           return None                
        
        subject = "Welcome " + self.new.title
        url = self.url (self.new)
        content = F"""Thank you for signing up. 
                      Here is your user url: {url}"""
        email = '"' + self.new.handle + '" <' + self.new.email + '>'
        self.notify (mailer.noReply,email, subject, content)
        #DO NOT SEND THE MAIL
        #IT Deletes the email.
        #Wait unti notify admin new user. 
        #self.sendTheMail()
        
    def notifyAdminsNewUser(self):
        self.mailer = mailer = self.parentalAcquire ("MailHost")
        if mailer == None:
           return ''                
        subject = "New User" 
        url = self.secureShortURL (context = self.new)        
        content = F"Here is the new user url {url}"
        self.notify (mailer.noReply, mailer.postMaster, subject, content)
        self.sendTheMail()

    def notifyAdminsNewVolunteer(self):
        self.mailer = mailer = self.parentalAcquire ("MailHost")
        if mailer == None:
           return ''                
        subject = "New Volunteer "
        subject += self.context.title
        url = self.secureShortURL (context = self.context)        
        content = F"{self.request.principal.title}"
        content += " is volunteering to help  {self.contextg.url}.  "
        content += "Just reply to this email."

        self.notify (mailer.noReply, mailer.postMaster, subject, content)
        self.sendTheMail()

    def notifyAdminsVolunteerResigned(self):
        self.mailer = mailer = self.parentalAcquire ("MailHost")
        if mailer == None:
           return ''                
        subject = "Volunteer Resigned From:"
        subject += self.context.title
        url = self.secureShortURL (context = self.context)        
        content = F"{self.request.principal.title}"
        content = " is resigning from  {self.contextg.url}.  "
        content += "Just reply to this email."        
        self.notify (mailer.noReply, mailer.postMaster, subject, content)
        self.sendTheMail()                

        
    def notifyAdminsNewPage(self):
        self.mailer = mailer = self.parentalAcquire ("MailHost")
        if mailer == None:
           return ''

        subject = "New " + self.new.__class__.__name__
        
        if self.treeSecurity():
           return
            
        elif self.isAuthenticated():
            subject += " By " + self.request.principal.title + " "
            subject += "Needs Approval" 
            
        else:
            subject += " By Anonymous Needs Approval "
            

        content = self.secureShortURL (context = self.new)
        self.notify (mailer.noReply,mailer.postMaster, subject, content)
        self.sendTheMail()

        
    def notifyAdminsPageDeleted(self):
        self.mailer = mailer = self.parentalAcquire ("MailHost")
        if mailer == None:
           return ''                        
        subject = "Page Deleted"
        content = self.request.url
        self.notify (mailer.noReply,mailer.postMaster, subject, content)       
        self.sendTheMail()


class SendMail(Notify):
    #def __init__(self, title):
    #    Action.__init__(self,title)
    
    def notifyEditors(self,data):
        self.mailer = mailer = self.parentalAcquire ("MailHost")
        if mailer == None:
           return ''                        
        subject = self.form.request['subject']
        content = self.form.request['text']
        to = self.geteditors()
        afrom = form.request.principal.email
        self.notify (afrom,to, subject, content)       
        self.sendTheMail()

    def getEditors(self):
        parents = self.form.parents()
        people = form.getPrincipalFolder()
        recipients = []
        for item in parents:
            if hasattr(item,'editors'):
               for person in item.editors:
                   if person in people:
                      email = people[person].email
                      recipients = recipients.append(email)
        result = ",".join(recipients)
        print (result)
        return result
    
    def __call__(self, form):
        self.form=form
        data, errors = self.form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE                
        self.notifyEditors(data)
        send ("Mail was sent")

@implementer (IMailHost)
class MailHost(Leaf):
    debug = False
    pass
    
@form_component
@name('addMailHost')
@context(IPage)
@implementer(ITreeSecurity)
class AddMailHost(AddNamedForm):
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
@name("edit")
@implementer(ITreeSecurity)
class EditMailHost(EditForm):
    subTitle='Edit the MailHost Object'    
