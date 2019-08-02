# -*- coding: utf-8 -*-

#This software is subject to the CV and Zope Public Licenses.
from zope.interface import Interface
from dolmen.forms.base import DISPLAY
from zopache.ttw.adduseractions  import Add
from zopache.crud.utils import getFactoryFields, getAllFields
from cromlech.i18n import translate

from cromlech.security import getSecurityGuards, permissions

from zopache.ttw.interfaces import IName, IContainer, ILeaf
from dolmen.container import BTreeContainer, IBTreeContainer
from zope.interface import implementer

from dolmen.forms.base import Actions
from dolmen.forms.base import Fields
from dolmen.forms.base import action, name, context, form_component

from zopache.crud.utilities import title_or_name    
from cromlech.webob import Response
from zopache.core.baseform import Form

from cromlech.browser.directives import title
from zopache.ttw.interfaces import IRegister
from zopache.ttw.principalfolder import InternalPrincipal
from zopache.ttw import tal_template

@form_component
@name (u'signup')
@context(Interface)
@title("Register")
class Register(Form):
    fields = Fields(IRegister)
    factory = InternalPrincipal
    title='PythonLinks.info'
    subTitle='Register Locally'
    ignoreContent = True
    igrnoreRequest = False
    
    
    def postAddProcess(self):
       if len(self.new.__parent__)==1:
           self.new.permissions = ['AddContent','EditContent',
            'Manage','Vote','Edit','Add']

    def acquireTitle(self):
       return 'Sign Up'
    
    def widgetDictionary(self):
        return {c.htmlId():c for c in self.bootstrap_widgets()}

    def fieldDictionary(self):
        return {c.__name__:c for c in self.fields}    

    @property
    def actions(self):
        return Actions(Add("Sign Me Up!",self))
    
    def newURL(self,new):
        #newURL = '/' + new.__name__ + "/support"
        newURL = "."
        return newURL

"""    
@form_component
@name (u'register')
@context(Interface)
@title("Register")
class RegisterShort(Register):
    fields = Fields(IRegisterShort)
    
    def nextUrl(self,new):
        newURL = '/'
        return newURL
"""
