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
from zopache.ttw.mail import Notify
from zopache.pages.interfaces import IPage

from zopache.crud.actions import Cancel


class BaseRegister(AddForm, Notify):
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

    def newURL(self,new):
        newURL = '..'        
        return newURL

    def postAddProcess(self):
        self.new.postAddProcess(view = self)
        
@form_component
@name (u'gregister')
@context(IPage)
class GRegister(BaseRegister):
    title='Site Registration'
    subTitle='Please enter your user id and GDPR permissions.'

    def postAddProcess(self):
        self.new.postAddProcess(view = self)
        text = "Thank you for registering."
        send (text)
        
#SUBSCRIBE    
@form_component
@name (u'subscribe')
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
        
#DONATE
@form_component
@name (u'donate')
@context(IPage)
class GDonate(BaseRegister):
    title='Site Registration'
    subTitle='Please enter your user id and GDPR permissions.'
    def newURL(self,new):
        newURL = '..'        
        return newURL

    def postAddProcess(self):
        self.new.postAddProcess(view = self)
        text = "Thank you for offering to donate to: "
        text += self.context.title
        text += ".  You will be contacted shortly."
        send (text)

#Volunteer
@form_component
@name (u'volunteer')
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
        

#ENDORSE
@form_component
@name (u'endorse')
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

        
