import subprocess
from pathlib import Path

from requests.models import urlencode

from cromlech.browser.exceptions import HTTPFound

from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.ttw.interfaces import IPrincipalFolder
from zopache.remote.mastodon.basebot import MastodonBot, TIMEOUT


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
        # credential file missing -> show error, re-render this page
        try:
            params = self.getParams()
        except FileNotFoundError:
            self.submissionErrors.append(
                "Github oauth credential file does not exist.")
            return

        params['redirect_uri'] = self.callbackURL()
        params['scope'] = ["read:user", "read:email"]

        endPoint = "https://github.com/login/oauth/authorize?"
        url = endPoint + urlencode(params)
        raise HTTPFound(url)

    
    def mastodonOauth(self):
        domain = self.getOauthServer()
        wikiDomain = self.getDomain().lower()        
        appDirectory = Path("/app/data/oauth") / wikiDomain
        secretFile = appDirectory / (domain + '.secret')
        errorURL = "/person/oauth?form.field.domain=" + domain
        if not secretFile.exists():
            appName = (self.getSiteRoot().title or (wikiDomain + "Oauth")).strip()
            try:
                subprocess.run(
                    ["python3", "/app/data/oauth/make_app.py",
                     wikiDomain, domain, appName],
                    timeout=TIMEOUT)
            except subprocess.TimeoutExpired:
                pass

        if not secretFile.exists():
            message = "Failed to create oauth appication. "
            self.sendMessage(message, type = "Error")                        
            raise HTTPFound(errorURL)
        # No error, all is good.
        try:
           mastodon= self.createMastodon(TIMEOUT)
           url = mastodon.auth_request_url(
                 redirect_uris = self.redirectURL(),
                 #   scopes=self.SCOPES,
                 force_login=False)
        except Exception as e:
            message = str(e)
            self.sendMessage(message, type = "Error")
            raise HTTPFound(errorURL)
        # No error, all is good - redirect outside the try so this
        # HTTPFound (itself an Exception, used for control flow) is
        # not caught by the except block above.
        raise HTTPFound(url)
            
    

