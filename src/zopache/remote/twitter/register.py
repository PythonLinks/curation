from dolmen.forms.base import Actions

from zopache.remote.twitter.actions import RegisterAction
from zopache.core.viewdecorators import *
from zopache.crud.actions import Cancel

@form_component
@name ('tregister')
@context(IServer)
class TwitterRegister(MastodonRegister):
    actions = Actions(
            RegisterAction("Please Register Me", "register"),
            Cancel("Cancel","Cancel")
            
        )
