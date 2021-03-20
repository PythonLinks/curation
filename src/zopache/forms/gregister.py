# -*- coding: utf-8 -*-
#Subject to the Zope Public License.

from dolmen.forms.base import Actions
from dolmen.message.utils import send

from zopache.core.viewdecorators import *

from zopache.ttw.gloginactions  import GoogleRegisterAction
from zopache.crud.utils import getFactoryFields, getAllFields
from zopache.pages.interfaces import INotPage

from zopache.ttw.interfaces import IName, IContainer, ILeaf
from dolmen.container import BTreeContainer, IBTreeContainer
from zope.interface import implementer

from zopache.crud.forms import AddForm
from dolmen.forms.base.markers import HIDDEN
from dolmen.forms.base.errors import Errors, Error
from zopache.forms.interfaces import IRegister, IGRegister, IGSubscribe
from zopache.ttw.principalfolder import InternalPrincipal
from zopache.ttw import tal_template
from zopache.forms.validator import GoogleValidator
from zopache.pages.interfaces import IPage

from zopache.crud.actions import Cancel
from zopache.ttw.mail import Notify

class BaseRegister(AddForm,Notify):
    
    dataValidators = [GoogleValidator]    
    count = 0
    layoutName = "UserMenu"    
    factory = InternalPrincipal
    fields = Fields(IGRegister)
    ignoreContent = True
    igrnoreRequest = False
    successfulRegistration = False
    submissionError = ""
    allowAnonymous = True

    def __init__(self,context,request):
        AddForm.__init__(self,context,request)
        Notify.__init__(self)

    def updateWidgets(self):
        self.fields["idtoken"].mode = HIDDEN        
        AddForm.updateWidgets(self)
        #if len (self.errors) == 1:
        #   self.errors.clear() 

    def breadcrumbs(self):
        return ''
    
    def acquireTitle(self):
        return 'GDPR Permissions'
    
    @property
    def actions(self):
        return Actions(
            Cancel("Cancel","Cancel"),            
            GoogleRegisterAction("Please Register Me", self))

    def postAddProcess(self):
        self.new.postAddProcess(view = self)
        
@form_component
@name (u'gregister')
@context(IPage)
class GRegister(BaseRegister):
    title='Site Registration'
    subTitle='Please enter your user id and GDPR permissions.'

    def newURL(self):
        newURL = "/" + self.context.__name__        
        return newURL

    def postAddProcess(self):
        self.new.postAddProcess(view = self)
        text = "Thank you for registering."
        send (text)
        
#SUBSCRIBE    
@form_component
@name (u'gsubscribe')
@context(IPage)
class GSubscribe(BaseRegister):
    title='Register To Subscribe'
    subTitle='Please enter your user id and GDPR permissions.'    
    fields = Fields(IGSubscribe)
        
    def postAddProcess(self):
        self.new.postAddProcess(view = self)
        text = "Thank you for subscribing. "
        text += self.context.title
        text += "We do not yet publish regularly. "
        send (text)
        
    def newURL(self):
        newURL = "/" + self.context.__name__ + "/subscribe"        
        return newURL
    
#DONATE
@form_component
@name (u'gdonate')
@context(IPage)
class GDonate(BaseRegister):
    title='Register To Donate'
    subTitle='Please enter your user id and GDPR permissions.'
    
    def newURL(self):
        newURL = '..'        
        return newURL

    def postAddProcess(self):
        self.new.postAddProcess(view = self)
        text = "Thank you for offering to donate to: "
        text += self.context.title
        text += ".  You will be contacted shortly."
        send (text)

    def newURL(self):
        newURL = self.acquireAttribute('donationsPageURL')
        if newURL == "": 
           "/" + self.context.__name__ 
        return newURL
    
#Volunteer
@form_component
@name (u'gvolunteer')
@context(IPage)
class GVolunteer(BaseRegister):
    title='Register To Volunteer'
    subTitle='Please enter your user id and GDPR permissions.'
    
    def postAddProcess(self):
        self.new.postAddProcess(view = self)
        text = "Thank you for volunteerng with "
        text += self.context.title
        text += ".  You will be contacted shortly."
        send (text)

    def newURL(self):
        newURL = "/" + self.context.__name__ + "/volunteer"        
        return newURL                

#ENDORSE
@form_component
@name (u'gendorse')
@context(IPage)
class GEndorse(BaseRegister):
    title='Register to Endorse This Candidate'
    subTitle='Please enter your user id and GDPR permissions.'
    
    def postAddProcess(self):
        self.new.postAddProcess(view = self)
        text =  "Thank you for endorsing "
        text += "self.context.title"
        text += "."
        send(text)
        
    def newURL(self):
        newURL = "/" + self.context.__name__ + "/endorse"        
        return newURL        
        
