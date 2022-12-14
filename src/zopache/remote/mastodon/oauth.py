from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.remote.mastodon.basebot import BaseBot
from cromlech.browser.exceptions import HTTPFound
from zopache.remote.mastodon.interfaces import IServer

@form_component
@context(IServer)
@target(IView)
@name("moauth")
class MastodonOauth(Form,BaseBot):
    title = "Authenticate with Mastodon.Social"
    subTitle = """Should you see this, it means their server is overloaded,
    plese try logging in again.. """
    #actions = Actions()
           
    def update(self):
        self.oauth()
