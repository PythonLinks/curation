from requests.models import urlencode

from cromlech.browser.exceptions import HTTPFound

from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.ttw.interfaces import IPrincipalFolder
from zopache.remote.mastodon.basebot import MastodonBot


@form_component
@context(IPrincipalFolder)
@target(IView)
@name("moauth")
class MastodonOauth(Form,MastodonBot):
    title = "Authenticate with Mastodon.Social"
    subTitle = """Should you see this, it means their server is overloaded,
    plese try logging in again.. """
    #actions = Actions()

    def update(self):
        oauthServer = self.getOauthServer()
        if oauthServer == "github.com":
            self.githubOauth()
        else:
            self.mastodonOauth()

    def githubOauth(self):
        # This reads the client id and secret
        mastodon= self.createMastodon()

        endPoint = "https://github.com/login/oauth/authorize?"
        params = dict()
        params['client_id'] = mastodon.client_id
        params['client_secret'] = mastodon.client_secret        
        params['redirect_uri'] = self.callbackURL()  
        params['scope'] = ["read:user", "read:email"]

        params = urlencode(params)
        url = endPoint + params
        raise HTTPFound(url)

    
    def mastodonOauth(self):
        mastodon= self.createMastodon()
        url = mastodon.auth_request_url(
            redirect_uris = self.redirectURL(),
            #scopes=self.SCOPES,
            force_login=False)
        raise HTTPFound(url)

    


