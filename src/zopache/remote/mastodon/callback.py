from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.pages.interfaces import IPageBase
from zopache.remote.mastodon.actions import CallBackAction
from zopache.remote.mastodon.basebot import BaseBot

@form_component
@context(IPageBase)
@target(IView)
@name("callback")
class MastodonOauth(Form, BaseBot):
    title = "Respond to the Oauth Callback "
    subTitle = "You should never see his. ."
    def update(self):
        CallBackAction("Redirect","redirect")(self)
        
    def render(self):
        breakpoint()        
