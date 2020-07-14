# -*- coding: utf-8 -*-

#This software is subject to the CV and Zope Public Licenses.
from zope.interface import Interface
from dolmen.forms.base import DISPLAY
from zopache.ttw.gloginactions  import GoogleLoginAction
from zopache.crud.utils import getFactoryFields, getAllFields
from cromlech.i18n import translate

from cromlech.security import getSecurityGuards, permissions

from zopache.ttw.interfaces import IName, IContainer, ILeaf
from zopache.forms.interfaces import IGLogin, IRegister
from dolmen.container import BTreeContainer, IBTreeContainer
from zope.interface import implementer

from dolmen.forms.base import Actions
from dolmen.forms.base import Fields
from dolmen.forms.base import action, name, context, form_component

from zopache.crud.utilities import title_or_name    
from cromlech.webob import Response
from zopache.core.baseform import Form

from cromlech.browser.directives import title
from zopache.ttw.principalfolder import InternalPrincipal
from zopache.ttw import tal_template

@form_component
@name (u'glogin')
@context(Interface)
@title("Google Login")
class GoogleLogin(Form):
    factory = InternalPrincipal
    title="Login Form"
    subTitle='Login: to be called from Javascript App'
    fields = Fields(IGLogin)
    ignoreContent = True
    igrnoreRequest = False
    loggedIn = False
    allowAnonymous = True    
    
    @property
    def actions(self):
        return Actions(GoogleLoginAction("Add", self))

    def updateWidgets(self):
        return Form.updateWidgets(self)

    def render (self,*args, **argv):
        if self.loggedIn:
           return "Success"
        else:
           return "Failed To Login."

    
