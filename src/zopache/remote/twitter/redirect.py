from cromlech.security import permissions
from dolmen.container import IBTreeContainer
from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.twitter.oauth import (twitter_get_oauth_request_token,
                                   )

@form_component
@context(IBTreeContainer)
@target(IView)
@name("twitterOauth")
class Clean(Form):
    title = "Login Using Twitter Oauth"
    subTitle = "You should never actually see this page"
    def update(self):

       result =  twitter_get_oauth_request_token()
       accessTokenList =  twitter_get_oauth_token(verifier, ro_key, ro_secret):
