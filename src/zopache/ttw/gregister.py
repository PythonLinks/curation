#Subject to the Non Compete MIT license
# -*- coding: utf-8 -*-

from dolmen.forms.base import Actions
from zopache.core.viewdecorators import *
#This software is subject to the CV and Zope Public Licenses.
from zopache.ttw.gloginactions  import GoogleRegisterAction
from zopache.crud.utils import getFactoryFields, getAllFields
from zopache.pages.interfaces import INotPage

from zopache.ttw.interfaces import IName, IContainer, ILeaf, IGRegister
from dolmen.container import BTreeContainer, IBTreeContainer
from zope.interface import implementer

from zopache.crud.forms import AddForm
from dolmen.forms.base.markers import HIDDEN

from zopache.ttw.interfaces import IRegister
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

    def doNothing(self):
        return ""



from dolmen.forms.base import Actions
from zopache.core.viewdecorators import *
#This software is subject to the CV and Zope Public Licenses.
from zopache.ttw.gloginactions  import GoogleRegisterAction
from zopache.crud.utils import getFactoryFields, getAllFields
from zopache.pages.interfaces import INotPage

from zopache.ttw.interfaces import IName, IContainer, ILeaf, IGRegister
from dolmen.container import BTreeContainer, IBTreeContainer
from zope.interface import implementer

from zopache.crud.forms import AddForm
from dolmen.forms.base.markers import HIDDEN

from zopache.ttw.interfaces import IRegister
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

    def doNothing(self):
        return ""
    submissionError = property (doNothing, doNothing)

    def updateWidgets(self):
        self.fields["idtoken"].mode = HIDDEN        
        AddForm.updateWidgets(self)
        widget = self.fieldWidgets['form.field.idtoken']

        pass
    
    def breadcrumbs(self):
        return ''
    
    
    def acquireTitle(self):
        return 'GDPR Permissions'
    
    @property
    def actions(self):
        return Actions(GoogleRegisterAction("Add", self))

    def newURL(self,new):
        if new.hirePermission:
            newURL = '/' + new.__name__ + "/edit"
        else:
            newURL = '/'
        return newURL
    
    """
    def nextURL(self):
        if (self.context.hiringPermissions == True):
           return "/
        if (self.context.hiringPermissions == True):
           return self.url(self.new) + "/edit"        
        else:
           return "."

        if not INotPage.providedBy(self.context):
           return '.'
        return self.url(self.new) + '/speakerregistration'

    """
    submissionError = property (doNothing, doNothing)

    def updateWidgets(self):
        import pdb; pdb.set_trace()        
        self.fields["idtoken"].mode = HIDDEN        
        AddForm.updateWidgets(self)
        widget = self.fieldWidgets['form.field.idtoken']

        pass
    
    def breadcrumbs(self):
        return ''
    
    
    def acquireTitle(self):
        return 'GDPR Permissions'
    
    @property
    def actions(self):
        return Actions(GoogleRegisterAction("Add", self))

    def newURL(self,new):
        if new.hirePermission:
            newURL = '/' + new.__name__ + "/edit"
        else:
            newURL = '/'
        return newURL
    
    """
    def nextURL(self):
        if (self.context.hiringPermissions == True):
           return "/
        if (self.context.hiringPermissions == True):
           return self.url(self.new) + "/edit"        
        else:
           return "."

        if not INotPage.providedBy(self.context):
           return '.'
        return self.url(self.new) + '/speakerregistration'

    """

from dolmen.forms.base import Actions
from zopache.core.viewdecorators import *
#This software is subject to the CV and Zope Public Licenses.
from zopache.ttw.gloginactions  import GoogleRegisterAction
from zopache.crud.utils import getFactoryFields, getAllFields
from zopache.pages.interfaces import INotPage

from zopache.ttw.interfaces import IName, IContainer, ILeaf, IGRegister
from dolmen.container import BTreeContainer, IBTreeContainer
from zope.interface import implementer

from zopache.crud.forms import AddForm
from dolmen.forms.base.markers import HIDDEN

from zopache.ttw.interfaces import IRegister
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

    def doNothing(self):
        return ""
    
    #submissionError = property (doNothing, doNothing)
    def updateWidgets(self):
        AddForm.updateWidgets(self)
        import pdb; pdb.set_trace()
        pass

    def breadcrumbs(self):
        return ''
        
    def acquireTitle(self):
        return 'GDPR Permissions'
    
    @property
    def actions(self):
        return Actions(GoogleRegisterAction("Add", self))

    def newURL(self,new):
        if new.hirePermission:
            newURL = '/' + new.__name__ + "/edit"
        else:
            newURL = '/'
        return newURL
    
    def updateWidgets(self):
        import pdb; pdb.set_trace()        
        self.fields["idtoken"].mode = HIDDEN        
        AddForm.updateWidgets(self)
        widget = self.fieldWidgets['form.field.idtoken']
        if len(self.errors) == 1:
             self.errors.clear()
        pass
    
    

