#Subject to the Non Compete MIT license
# -*- coding: utf-8 -*-

from dolmen.forms.base import Actions
from zopache.core.viewdecorators import *
#This software is subject to the CV and Zope Public Licenses.
from zopache.ttw.gloginactions  import GoogleRegisterAction
from zopache.crud.utils import getFactoryFields, getAllFields
from zopache.pages.interfaces import INotPage

from zopache.ttw.interfaces import IName, IContainer, ILeaf
from dolmen.container import BTreeContainer, IBTreeContainer
from zope.interface import implementer

from zopache.crud.forms import AddForm
from dolmen.forms.base.markers import HIDDEN

from zopache.forms.interfaces import IRegister, IGRegister
from zopache.ttw.principalfolder import InternalPrincipal
from zopache.ttw import tal_template

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
    submissionError = ""
    
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
        return Actions(GoogleRegisterAction("Please Register Me", self))

    def newURL(self,new):
        if new.hirePermission:
            newURL = '/' + new.__name__ + "/edit"
        else:
            newURL = '/'
        return newURL
    
