from cromlech.browser.exceptions import HTTPFound
from mastodon import Mastodon
from cromlech.security import unauthenticated_principal as anonymous

class BaseBot (object):
    SCOPES = ['read:accounts','write:media','write:statuses']
    
    def proxyForUser(self):
        principal = self.request.principal
        if principal == anonymous:
            self.oauth()
        proxy = getattr (principal,'accountProxy',None)
        if proxy == None:
            self.oauth()
        return proxy

    def userProxy(self,accessToken):
        context = self.context
        mastodonDomain = context.__NAME__
        mastodon =   Mastodon(
            access_token = accessToken.strip(),
            scopes = form.SCOPES,
            #debug_requests = True,
            api_base_url = "https://" + mastodonDomain)
        return mastodon 
    
    def baseURL(self):
        result =self.getSecureLongURL(context = self.context)             
        print ("\n\n"+result + "\n\n")
        return result
    
    def redirectURL(self):
        result =   self.baseURL() + '/callback'
        return result
    
    def registerURL(self):
        return self.baseURL() + '/register?'
        
    def oauthProxy(self):
        context = self.context
        return  Mastodon(
            access_token = context.accessToken.strip(),
            client_id = context.clientKey.strip(),
            client_secret = context.clientSecret.strip(),
            api_base_url = "https://" + context.__name__)

    def oauth(self):
        breakpoint()
        proxy = self.oauthProxy()
        url = proxy.auth_request_url(
            redirect_uris= self.redirectURL(),
            scopes=self.SCOPES,
            force_login=False)
        raise HTTPFound(url)


#    def myAccount(self):
#        with open('/app/data/accessToken') as file:
#            accessToken = file.readline()
#            
#        context = self.context 
#        proxy = Mastodon(
#            client_id = context.clientKey.strip(),
#            client_secret = context.clientSecret.strip(),
#            access_token = accessToken,
#            api_base_url='https://mastodon.social',
#            debug_requests=False,
#            ratelimit_method='wait',
#            ratelimit_pacefactor=1.1,
#            request_timeout=300, 
#            mastodon_version=None,
#            version_check_mode='created',
#            session=None,
#            feature_set='mainline')
#        return proxy
