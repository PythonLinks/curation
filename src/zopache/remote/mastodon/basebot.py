from cromlech.browser.exceptions import HTTPFound
from mastodon import Mastodon
from cromlech.security import unauthenticated_principal as anonymous

class BaseBot(object):
    SCOPES = ['read:accounts','write:media','write:statuses']

    def myAccount(self):
        with open('/app/data/accessToken') as file:
            accessToken = file.readline()

        proxy = Mastodon(
            client_id=None,
            client_secret=None,
            access_token = accessToken,
            api_base_url='https://mastodon.social',
            debug_requests=False,
            ratelimit_method='wait',
            ratelimit_pacefactor=1.1,
            request_timeout=300, 
            mastodon_version=None,
            version_check_mode='created',
            session=None,
            feature_set='mainline')
        return proxy
   
    def oauth(self):    
        url = self.oauthProxy().auth_request_url(
            redirect_uris= self.redirectURL(),
            scopes=self.SCOPES,
            force_login=False)
        raise HTTPFound(url)

    def getProxy (self,accessToken,clientId,clientSecret,mastodonDomain):
        return  Mastodon(
            access_token = accessToken.strip(),
            client_id = clientId.strip(),
            client_secret = clientSecret.strip(),
            api_base_url = "https://" + mastodonDomain)

    def userProxy(self,accessToken):
        context = self.context
        mastodonDomain = context.mastodonDomain
        mastodon =   Mastodon(
            access_token = accessToken.strip(),
            api_base_url = "https://" + mastodonDomain)
        return mastodon 

    def proxyForUser(self):
        principal = self.request.principal
        if principal == anonymous:
            self.oauth()
        proxy = getattr (principal,'accountProxy',None)
        if proxy == None:
            self.oauth()
        return proxy
    
    def oauthProxy(self):
        context = self.context
        accessToken = context.accessToken
        clientSecret = context.clientSecret
        clientId = context.clientKey
        mastodonDomain = context.mastodonDomain
        return self.getProxy(accessToken, clientId, clientSecret, mastodonDomain)

    def baseURL(self):    
        domain = self.getDomain()
        url = ("https://"+
           domain +
           '/servers/')
        #if domain == "dev.pythonlinks.info":
        #    url += domain + '/'
        url += self.context.name
        return url
    
    def redirectURL(self):
        result =   self.baseURL() + '/callback'
        return result
    
    def registerURL(self):
        return self.baseURL() + '/register?'
        

        
