# -*- coding: utf-8 valida-*-
from zope.interface import Interface

#This software is subject to the CV and Zope Public Licenses.
from cromlech.webob import Response
from dolmen.forms.base import Actions
from dolmen.forms.base import Fields
from dolmen.forms.base import action, name, context, form_component

from zopache.crud.actions import Cancel
from zopache.crud.forms import BasicForm
from zopache.forms.adduseractions  import RegisterAction, SubscribeAction
from zopache.crud.utils import getFactoryFields, getAllFields

from zopache.forms.interfaces import IRegister, ISubscribe
from zopache.ttw.principalfolder import InternalPrincipal
from zopache.forms.validator import Validator
from zopache.ttw.mail import Notify

@form_component
@name ('register')
@context(Interface)
class Register(BasicForm):
    dataValidators = [Validator]
    layoutName = "UserMenu"
    fields = Fields(IRegister)
    factory = InternalPrincipal
    title='Register'
    subTitle='To stay in touch, or to become an editor.'
    allowAnonymous = True
        
    def acquireTitle(self):
       return 'Sign Up'
    
    @property
    def actions(self):
        return Actions(
               RegisterAction("Sign Me Up!","register"),
               Cancel("Cancel","Cancel")
        )
    
    def newURL(self,new):
        newURL = "."
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
