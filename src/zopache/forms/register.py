# -*- coding: utf-8 -*-

#This software is subject to the CV and Zope Public Licenses.
from zope.interface import Interface
from zope.interface import implementer
from dolmen.forms.base import DISPLAY
from cromlech.i18n import translate
from dolmen.container import BTreeContainer, IBTreeContainer
from cromlech.security import getSecurityGuards, permissions
from cromlech.webob import Response
from dolmen.forms.base import Actions
from dolmen.forms.base import Fields
from dolmen.forms.base import action, name, context, form_component
from cromlech.browser.directives import title


from zopache.forms.adduseractions  import Add
from zopache.crud.utils import getFactoryFields, getAllFields

from zopache.ttw.interfaces import IName, IContainer, ILeaf


from zopache.crud.utilities import title_or_name    
from zopache.core.baseform import Form
from zopache.core.breadcrumbs import Breadcrumbs

from zopache.forms.interfaces import IRegister
from zopache.ttw.principalfolder import InternalPrincipal
from zopache.ttw import tal_template
from zopache.crud.actions import Cancel
from zopache.forms.validator import Validator
from zopache.ttw.mail import Notify

@form_component
@name ('signup')
@context(Interface)
class Register(Form,Notify,Breadcrumbs):
    dataValidators = [Validator]
    layoutName = "UserMenu"
    fields = Fields(IRegister)
    factory = InternalPrincipal
    title='Register'
    subTitle='Register Locally'
    ignoreContent = True
    igrnoreRequest = False
    count = 0
    allowAnonymous = True

    def __init__(self,context,request):
        Form.__init__(self,context,request)
        Notify.__init__(self)

    """    
    def update(self):
        if self.getDomain() in [ "dev.pythonlinks.info",
            "news.uncensorednews.us"]:
             return
         
        if not self.getSiteRoot().localLogin:
            self.raiseUnauthorized()
    """
    
    def acquireTitle(self):
       return 'Sign Up'
    
    def widgetDictionary(self):
        return {c.htmlId():c for c in self.bootstrap_widgets()}

    def fieldDictionary(self):
        return {c.__name__:c for c in self.fields}    

    @property
    def actions(self):
        return Actions(Add("Sign Me Up!",self),
               Cancel("Cancel","Cancel")
        )
    
    def newURL(self,new):
        #newURL = '/' + new.__name__ + "/support"
        newURL = "."
        return newURL

