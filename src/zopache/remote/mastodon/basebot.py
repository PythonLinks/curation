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

    def getOauthServer(self):
        return self.request.form['oauth-server']

    def redirectURL(self):
         return self.callbackURL()
     
    def callbackURL(self):
        domain = self.getDomain()
        oauthServer = self.getOauthServer()
        result = ("https://"+
                  domain +
                  '/person/callback/'+
                  oauthServer
                  )
        return result

    
    def createMastodon(self):
        context = self.context
        fileName =  ("/app/data/oauth/" +
                    self.getDomain() +
                    "/" +
                    self.getOauthServer() + 
                    ".secret")
        mastodon = Mastodon(client_id = fileName,)
        return mastodon

    def getParams(self):
        mastodon  = self.createMastodon()        
        params = dict()
        params['client_id'] = mastodon.client_id
        params['client_secret'] = mastodon.client_secret
        return params
    
class MastodonBot(BaseBot):
    SCOPES = ['read:accounts','write:media','write:statuses']

    def userLoginProxy(self,code):
        context = self.context
        mastodon  = self.createMastodon()
        result = mastodon.log_in( code = code ,
                               #scopes = self.SCOPES,
                               redirect_uri= self.callbackURL())
        return mastodon
    

