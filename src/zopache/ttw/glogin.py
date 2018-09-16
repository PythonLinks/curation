# -*- coding: utf-8 -*-

#This software is subject to the CV and Zope Public Licenses.
from zope.interface import Interface
from dolmen.forms.base import DISPLAY
from .gloginactions  import GoogleLoginAction
from zopache.crud.utils import getFactoryFields, getAllFields
from cromlech.i18n import translate

from cromlech.security import getSecurityGuards, permissions

from zope.cachedescriptors.property import CachedProperty
from .interfaces import IName, IContainer, ILeaf, IGLogin
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
@name (u'glogin')
@context(Interface)
@title("Google Login")
class GoogleLogin(Form):
    factory = InternalPrincipal
    title='PythonLinks.info'
    subTitle='Login: to be called from Javascript App'
    fields = Fields(IGLogin)
    ignoreContent = True
    igrnoreRequest = False
    loggedIn = False
    
    def debug(self,widget):
        import pdb; pdb.set_trace()
        pass


    @CachedProperty
    def actions(self):
        return Actions(GoogleLoginAction("Add", self))

    def updateWidgets(self):
        return Form.updateWidgets(self)

    def render (self,*args, **argv):
        if self.loggedIn:
           return "Success"
        return Form.render(self,*args, **argv)
    
