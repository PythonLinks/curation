# -*- coding: utf-8 -*-
#Subject to the Zope Public License.


from dolmen.forms.base import Actions, Fields

from zopache.core.viewdecorators import *

from zopache.crud.forms import AddForm
from dolmen.forms.base.markers import HIDDEN, DISPLAY
from dolmen.forms.base.errors import Errors, Error
from zopache.remote.mastodon.interfaces import IRegister
from zopache.ttw.principalfolder import InternalPrincipal
from zopache.crud.actions import Cancel
from zopache.ttw.mail import Notify
from zopache.business.exists import DuplicatePerson

from zopache.remote.mastodon.interfaces import IServer
from zopache.remote.mastodon.account import Account
from zopache.remote.mastodon.actions import MastodonRegisterAction
from zopache.remote.mastodon.basebot import BaseBot

@form_component
@name ('register')
@context(IServer)
class MastodonRegister(AddForm,Notify,BaseBot):
    count = 0
    #dataValidators = [DuplicatePerson]
    layoutName = "UserMenu"    
    factory = Account
    fields = Fields(IRegister)
    ignoreContent = True
    igrnoreRequest = False
    successfulRegistration = False
    submissionError = ""
    allowAnonymous = True
    interface = IRegister
    subTitle = "Please review your account, and grant the site your GDPR permission. "
    
    def __init__(self,context,request):
        AddForm.__init__(self,context,request)
        Notify.__init__(self)
        
    def updateWidgets(self):
        self.fields["accessToken"].mode = HIDDEN
        AddForm.updateWidgets(self)        

    def acquireTitle(self):
        return 'GDPR Permissions'
    
    actions = Actions(
            MastodonRegisterAction("Please Register Me", "register"),
            Cancel("Cancel","Cancel")
            
        )

    def postAddProcess(self):
        self.new.postAddProcess(view = self)
