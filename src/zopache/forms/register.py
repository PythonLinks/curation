# -*- coding: utf-8 valida-*-
from zope.interface import Interface

#This software is subject to the CV and Zope Public Licenses.
from dolmen.forms.base import Actions
from dolmen.forms.base import Fields
from dolmen.forms.base import action, name, context, form_component

from zopache.crud.actions import Cancel
from zopache.crud.forms import EditGDPR
from zopache.forms.adduseractions  import RegisterAction, SubscribeAction
from zopache.crud.utils import getFactoryFields, getAllFields

from zopache.forms.interfaces import IPermissions, ISubscribe
from zopache.forms.gdpr_validator import GDPRValidator
from zopache.crud.forms import EditForm

@form_component
@name ('gdpr')
@context(Interface)
class Register(EditGDPR):
    dataValidators = [GDPRValidator]
    layoutName = "UserMenu"
    fields = Fields(IPermissions)
    title='GDPR Permissions'
    subTitle='Please edit your GDPR permissions.'
    allowAnonymous = False
        
    def acquireTitle(self):
       return 'Permissions Page'

    def newURL(self,new):
        newURL = "/connect"
        return newURL
    
@form_component
@name ('subscribe')
@context(Interface)
class Subscribe (Register):
    fields = Fields(ISubscribe)
    title = 'Subscribe'
    subTitle = 'To the uncensored newsletter'

    def acquireTitle(self):
       return 'Subscribe'
   
    @property
    def actions(self):
        return Actions(SubscribeAction("Sign Me Up!",self),
               Cancel("Cancel","Cancel")
        )
