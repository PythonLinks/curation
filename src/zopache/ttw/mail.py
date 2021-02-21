#CURRENTLY JUST TO A SINGLE PERSON
#CURRENTLY ONLY USES MAIL QUEUE
from time import time
from email.message import Message
from subprocess import Popen
import random
import os

from zope import schema
from repoze.sendmail.delivery import QueuedMailDelivery
from z3c.schema.email  import RFC822MailAddress as Email


from zopache.core.viewdecorators import *
from zopache.core import Leaf
from zopache.crud.interfaces import ILeaf
from zopache.pages.interfaces import IPage
from zopache.crud.forms import AddByNameForm, EditForm
from zopache.core.interfaces import ITreeSecurity
from zopache.ttw.interfaces import IMailHost
from zopache.core.transactionnote import TransactionNote

from here import HERE
dataDir = os.path.join(HERE, 'data')


class Notify (TransactionNote):
    sender ='"Green Maps Newsletter" <lozinski@PythonLinks.info>'
    
    def setMailer(self):
       self.mailer = mailer = self.parentalAcquire ("MailHost")
    
    def getRecentArticles(self,principal):
        articles = self.context.bestMostRecentPage()
        recentArticles = []
        lastNotificationTime = principal.lastNotificationTime
        for item in articles:
            if item.creationTime > lastNotificationTime:
                recentArticles.append(item)
        return recentArticles

    def canSend(self,principal):
        currentTime = time()
        lastNotificationTime = principal.lastNotificationTime
        frequency =getattr(principal,'frequencyPermission','')
            
        newsPermission = getattr(principal,'newsPermission','')
        
        if (frequency =='Never'): 
            return False
        
        elif (frequency == 'Weekly'):
            if (currentTime - lastNotificationTime) > (3600*24 *7):
                return True
            
        elif (frequency == 'Seldom'):
            if (currentTime - lastNotificationTime) > (3600*24 * 31 * 3):
                return True            
            
        elif (frequency == 'Monthly'):
            if (currentTime - lastNotificationTime) > (3600*24 * 31):
                return True

        elif (frequency == 'Weekly'):
            if (currentTime - lastNotificationTime) > (3600*24 * 1):
                return True
            
        if hasattr(principal,'newsPermission'):
            if principal.newsPermission == True:
                return True
            
        return False
    
    def broadcastNews(self):
        self.setMailer()
        people = self.parentalAcquire('person')
        for item in people.values():
            self.sendToPrincipal(item)
        self.sendTheMail()
        
    def sendMeANewsletter(self):
        self.setMailer()        
        principal = self.request.principal
        self.sendToPrincipal(principal)
        self.sendTheMail()
        
    def sendToPrincipal(self,principal): 
        text = "NewsLetter:"
        text += self.context.newsTitle
        to = principal.email
        articles = self.getRecentArticles(principal)
        
        if len(articles) == 0:
            return
        
        if not self.canSend(principal):
            return
        
        principal.lastNotificationTime = time()        
        self.describeTransactionWithText(text)
        self.createOneNewsletter(to, self.sender, articles)

    
    def createOneNewsletter(self, to, sender, articles):
        self.mailer = mailer = self.parentalAcquire ("MailHost")
        if mailer == None:
           return ''

        subject = self.context.newsTitle


        self.notify (sender,
                     to,
                     subject,
                     self.context.preAmble,
                     articles = articles)
        

        
    def articlesAsText(self,articles):
        random.shuffle(articles)
        result = ""
        count = 0
        theTime = time()
        for article in articles:
            count += 1
            result += str(count)
            result += ". "
            result += article.title
            result += " "            
            result += str((time() - article.creationTime)/(3600*24))[0:3]
            result +=" days \n"
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
        self.setMailer()        
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
        self.setMailer()        

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
        self.setMailer()        
        if mailer == None:
           return ''                
        subject = "New User" 
        url = self.secureShortURL (context = self.new)        
        content = F"Here is the new user url {url}"
        self.notify (mailer.noReply, mailer.postMaster, subject, content)
        self.sendTheMail()

    def notifyAdminsMembershipEvent(self,subject):
        self.setMailer()
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
        self.setMailer()                
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
        self.setMailer()                        
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
@name("edit")
@implementer(ITreeSecurity)
class EditMailHost(EditForm):
    subTitle='Edit the MailHost Object'    
 
    """    
    def sendOneNewsletter(self):
        to = mailer.postMaster
        articles = self.context.bestMostRecentPage()
        self.createOneNewsLetter(to, self.sender, articles)
        self.sendTheMail()
    """
