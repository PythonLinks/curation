#Subject to the Non Compete MIT license
# -*- coding: utf-8 -*-

from zope.cachedescriptors.property import CachedProperty
from dolmen.forms.base import Actions
from zopache.core.viewdecorators import *
#This software is subject to the CV and Zope Public Licenses.
from .gloginactions  import GoogleRegisterAction
from zopache.crud.utils import getFactoryFields, getAllFields

from .interfaces import IName, IContainer, ILeaf, IGRegister
from dolmen.container import BTreeContainer, IBTreeContainer
from zope.interface import implementer

from zopache.crud.forms import AddForm

from .interfaces import IRegister
from .principalfolder import InternalPrincipal
from . import tal_template

@form_component
@name (u'gregister')
@context(Interface)
@title("Google Register")
class GoogleRegister(AddForm):
    factory = InternalPrincipal
    title='PythonLinks.info'
    subTitle='Register'
    fields = Fields(IGRegister)
    ignoreContent = True
    igrnoreRequest = False
    successfulRegistration = False
    template = tal_template('gregister.pt')

    def breadcrumbs(self):
        return ''
    
    
    def acquireTitle(self):
        return 'GDPR Permissions'
    
    @CachedProperty
    def actions(self):
        return Actions(GoogleRegisterAction("Add", self))


    def nextURL(self):

        return self.url(self.new) + '/meetupspeaker'        
        if (self.context.hiringPermissions == True):
           return "./submitJob"
       
        elif (self.context.hiringPermissions == True):
           return "./submitResume"        
        else:
            return "."

