#CURRENTLY JUST TO A SINGLE PERSON
#CURRENTLY ONLY USES MAIL QUEUE
from email.message import Message
from subprocess import Popen
import random
        
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



from here import HERE
dataDir = os.path.join(HERE, 'data')
class Notify (object):
    
    def sendOneNewsletter(self):
        self.mailer = mailer = self.parentalAcquire ("MailHost")
        if mailer == None:
           return ''

        subject = self.context.newsTitle
        breakpoint()
        articles = self.context.bestMostRecentPage()

        self.notify (mailer.noReply,
                     mailer.postMaster,
                     subject,
                     self.context.preAmble,
                     articles = articles)
        
        self.sendTheMail()
        
    def articlesAsText(self,articles):
        random.shuffle(articles)
        result = ""
        count = 0
        for article in articles:
            count += 1
            result += str(count)
            result += ". "
            result += article.title
            result +="\n"
        result +="\n\n"

        count = 0    
        for article in articles: 
            count +=1
            result += str(count)
            result += ". "            
            result += article.title
            result +="\n"            
            result += article.description
            result +="\n"            
            if getattr(article,'remoteURL',False):
               result += article.remoteURL
            else:
                result += self.secureShortURL (context = article)
            result +="\n\n"
        return result
    
    def notify (self,aFrom,to, subject, content, articles = []):
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
        articlesAsText = self.articlesAsText(articles)
        message.set_payload(content + "\n\n" + articlesAsText)
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
        #print (' '.join (command))
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

    def notifyAdminsMembershipEvent(self,subject):
        self.mailer = mailer = self.parentalAcquire ("MailHost")
        if mailer == None:
           return ''                
        subject += self.context.title
        url = self.secureShortURL (context = self.context)

        content = F"{subject} \n {self.request.principal.title} \n"
        content += f" {self.secureShortURL(self.context)}.  \n"
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
        content = f" is resigning from  {self.context.url}.  "
        content += "Just reply to this email."        
        self.notify (mailer.noReply, mailer.postMaster, subject, content)
        self.sendTheMail()                

        
    def notifyAdminsPageDeleted(self):
        self.mailer = mailer = self.parentalAcquire ("MailHost")
        if mailer == None:
           return ''                        
        subject = "Page Deleted"
        content = self.request.url
        self.notify (mailer.noReply,mailer.postMaster, subject, content)       
        self.sendTheMail()
        

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
 
