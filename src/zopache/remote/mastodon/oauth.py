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
    subTitle = "You should never see this. "
    #actions = Actions()
           
    def update(self):
        url = self.oauthProxy().auth_request_url(
            redirect_uris= self.redirectURL(),
            scopes=self.SCOPES,
            force_login=False)
        raise HTTPFound(url)
