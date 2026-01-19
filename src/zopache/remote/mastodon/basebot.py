from cromlech.browser.exceptions import HTTPFound
from mastodon import Mastodon
from cromlech.security import unauthenticated_principal as anonymous

class BaseBot (object):

    def proxyForUser(self):
        principal = self.request.principal
        if principal == anonymous:
            self.oauth()
        proxy = getattr (principal,'accountProxy',None)
        if proxy == None:
            self.oauth()
        return proxy

    def redirectURLFromURL(self):
        domain = self.getDomain()
        breakpoint()
        result = ("https://"+
                  domain +
                  '/oauth/' +
                  domain +
                  '/'  +
                  self.context.mastodonDomainName()+
                  '/callback')
        return result


class MastodonBot(BaseBot):
    SCOPES = ['read:accounts','write:media','write:statuses']

    def createMastodon(self):
        context = self.context
        apiServer = context.mastodonDomainName()        
        fileName =  ("/app/data/oauth/" +
                    self.getDomain() +
                    "/" +
                    apiServer + 
                    ".secret")
        mastodon = Mastodon(client_id = fileName,)
        return mastodon
    
    def oauth(self):
        mastodon= self.createMastodon()
        url = mastodon.auth_request_url(
            redirect_uris = self.redirectURL(),
            #scopes=self.SCOPES,
            force_login=False)
        raise HTTPFound(url)


    def userLoginProxy(self,code):
        context = self.context
        mastodon  = self.createMastodon()
        result = mastodon.log_in( code = code ,
                               #scopes = self.SCOPES,
                               redirect_uri= self.redirectURL())
        return mastodon
    
class DiscordBot(BaseBot):    
   pass

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
