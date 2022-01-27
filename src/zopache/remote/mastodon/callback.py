from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.remote.mastodon.interfaces import IServer
from zopache.remote.mastodon.actions import MastodonCallBackAction
from zopache.remote.mastodon.basebot import BaseBot

@form_component
@context(IServer)
@target(IView)
@name("callback")
class MastodonOauth(Form, BaseBot):
    title = "Respond to the Oauth Callback "
    subTitle = "You should never see his. ."
    def update(self):
        CallBackAction("Redirect","redirect")(self)
        
