# -*- coding: utf-8 -*-

#This software is subject to the CV and Zope Public Licenses.
from zope.interface import Interface
from dolmen.forms.base import DISPLAY
from .gloginactions  import GoogleRegisterAction
from zopache.crud.utils import getFactoryFields, getAllFields
from cromlech.i18n import translate

from cromlech.security import getSecurityGuards, permissions

from zope.cachedescriptors.property import CachedProperty
from .interfaces import IName, IContainer, ILeaf, IGRegister
from dolmen.container import BTreeContainer, IBTreeContainer
from zope.interface import implementer

from dolmen.forms.base import Actions
from dolmen.forms.base import Fields
from dolmen.forms.base import action, name, context, form_component

from zopache.crud.utilities import title_or_name    
from cromlech.webob import Response
from zopache.core.baseform import Form

from cromlech.browser.directives import title
from .interfaces import IRegister
from .principalfolder import InternalPrincipal
from . import tal_template

@form_component
@name (u'gregister')
@context(Interface)
@title("Google Register")
class GoogleRegister(Form):
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
    
    def debug(self,widget):
        import pdb; pdb.set_trace()
        pass
    
    def acquireTitle(self):
        return 'GDPR Permissions'
    
    @CachedProperty
    def actions(self):
        return Actions(GoogleRegisterAction("Add", self))

    def updateWidgets(self):
        return Form.updateWidgets(self)

    def nextURL(self):
        return "."        
        if (self.context.hiringPermissions == True):
           return "./submitJob"
       
        elif (self.context.hiringPermissions == True):
           return "./submitResume"        
        else:
            return "."

