# -*- coding: utf-8 -*-

#This software is subject to the CV and Zope Public Licenses.
from zope.interface import Interface
from zope.interface import implementer
from zope.cachedescriptors.property import CachedProperty


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
from .interfaces import ILogin , IPrincipalFolder
from dolmen.forms.base.errors import Error
from cromlech.browser.exceptions import HTTPFound
from zopache.core import getRoot

@form_component
@name (u'login')
@context(Interface)
@title("Login")
class LoginForm(Form):
    """ Used to login
    """
    title='PythonLinks.info'
    subTitle='Please Login'
    fields = Fields(ILogin)
    ignoreContent = True
    submissionError = []
    def getContext(self):
      root = getRoot(self.context)
      return root ["person"]
  
    @action('Log Me In')
    def login(self):
        data, errors = self.extractData()
        if errors:
            self.form.errors = errors
            return FAILURE
        
        success = self.getContext().authenticate(data)
        if success == None:
            self.errors.append(Error(
                title='Login failed',
                identifier=self.prefix,
            ))
            return FAILURE
        raise HTTPFound(".")
##
        #return SuccessMarker('Added', True, url="..",code=307)

        #raise HTTPFound(url)


