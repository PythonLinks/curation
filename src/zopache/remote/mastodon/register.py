# -*- coding: utf-8 -*-
#Subject to the Zope Public License.


from dolmen.forms.base import Actions, Fields
from dolmen.message.utils import send

from zopache.core.viewdecorators import *

from zopache.crud.forms import AddForm
from dolmen.forms.base.markers import HIDDEN, DISPLAY
from dolmen.forms.base.errors import Errors, Error
from zopache.remote.mastodon.interfaces import IRegister
from zopache.ttw.principalfolder import InternalPrincipal
from zopache.crud.actions import Cancel
from zopache.ttw.mail import Notify
from zopache.business.exists import DuplicatePerson

class MastodonRegister(AddForm,Notify):
    count = 0
    dataValidators = [DuplicatePerson]
    layoutName = "UserMenu"    
    factory = InternalPrincipal
    fields = Fields(IRegister)
    ignoreContent = True
    igrnoreRequest = False
    successfulRegistration = False
    submissionError = ""
    allowAnonymous = True

    def __init__(self,context,request):
        AddForm.__init__(self,context,request)
        Notify.__init__(self)

    def updateWidgets(self):
        self.fields["accessToken"].mode = HIDDEN
        self.fields["userName"].mode = DISPLAY
        self.fields["displayName"].mode = DISPLAY
        self.fields["serverName"].mode = DISPLAY        
        self.fields["email"].mode = DISPLAY        
        
        AddForm.updateWidgets(self)

    def acquireTitle(self):
        return 'GDPR Permissions'
    
    @property
    def actions(self):
        return Actions(
            RegisterAction("Please Register Me", self),
            Cancel("Cancel","Cancel")
            
        )

    def postAddProcess(self):
        self.new.postAddProcess(view = self)
