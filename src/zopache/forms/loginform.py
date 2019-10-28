# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.interface import implementer

from dolmen.forms.base import Actions
from dolmen.forms.base import Fields
from dolmen.forms.base import action, name, context, form_component
from cromlech.browser.directives import title
from cromlech.webob import Response
from cromlech.security import getSecurityGuards, permissions

from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base.markers import FAILURE
from cromlech.browser import IURL

from zopache.crud.utilities import title_or_name    
from zopache.core.baseform import Form
from zopache.crud.utils import getFactoryFields, getAllFields
from zopache.crud.interfaces import IName, IContainer, ILeaf
from zopache.ttw.interfaces import IPrincipalFolder
from zopache.forms.interfaces import ILogin
from dolmen.forms.base.errors import Error
from cromlech.browser.exceptions import HTTPFound
from zopache.core.getroot import getPrincipalFolder

  
class LoginAction(Action):

    def __call__(self,form):
        data, errors = form.extractData()
        if errors:
            form.errors = errors
            return FAILURE
        success = self.getContext(form).authenticate(data)
        if success == None:
            form.errors.append(Error(
                title='Login failed',
                identifier=self.prefix,
            ))
            return FAILURE
        raise HTTPFound(".")
##
        #return SuccessMarker('Added', True, url="..",code=307)

        #raise HTTPFound(url)

    def getContext(self,form):
        return getPrincipalFolder(form.context)

@form_component
@name (u'login')
@context(Interface)
@title("Login")
class LoginForm(Form):
    """ Used to login
    """
    layoutName = "NoMenuLayout"
    title='Log in '
    subTitle='Please Login'
    fields = Fields(ILogin)
    ignoreContent = True
    submissionError = []

    @property
    def actions(self):
        return Actions(
            LoginAction("Log In","Log In"))
            
