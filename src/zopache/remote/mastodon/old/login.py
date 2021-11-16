# -*- coding: utf-8 -*-


from zope.interface import Interface
from zope.interface import implementer

from dolmen.forms.base import DISPLAY
from cromlech.webob import Response
from dolmen.container import BTreeContainer, IBTreeContainer

from zopache.core.viewdecorators import *
from zopache.ttw.gloginactions  import GoogleLoginAction
from zopache.crud.utils import getFactoryFields, getAllFields
from zopache.ttw.interfaces import IName, IContainer, ILeaf
from zopache.forms.interfaces import IGLogin, IRegister
from zopache.crud.utilities import title_or_name    
from zopache.core.baseform import Form
from zopache.ttw.principalfolder import InternalPrincipal
from zopache.ttw import tal_template

@form_component
@name (u'glogin')
@context(Interface)
class MastodonLogin(Form):
    factory = InternalPrincipal
    title="Mastodon Login Form"
    subTitle='Login: to be called from Javascript App'
    fields = Fields(IGLogin)
    ignoreContent = True
    igrnoreRequest = False
    loggedIn = False
    allowAnonymous = True    
    
    @property
    def actions(self):
        return Actions(GoogleLoginAction("Add", self))


    def render (self,*args, **argv):
        if self.loggedIn:
           return "Success"
        else:
           return "Failed To Login."

    
