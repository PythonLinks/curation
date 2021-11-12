from mastodon import Mastodon

class BaseBot(object):
    SCOPES = ['read:accounts','write:media','write:statuses']

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
        proxy = getattr (self.request.principal,'accountProxy',None)        
        if proxy == None:
           raise Exception("First you need to log in to a Mastodon server. ")
        return proxy
    
    def oauthProxy(self):
        context = self.context
        accessToken = context.accessToken
        clientSecret = context.clientSecret
        clientId = context.clientKey
        mastodonDomain = context.mastodonDomain
        return self.getProxy(accessToken, clientId, clientSecret, mastodonDomain)

    def redirectURL(self):
        url = ("https://"+
           self.getDomain()+
           '/servers/' +
           self.context.name +
           '/callback')
        return url

    def registerURL(self):
        url = ("https://"+
           self.getDomain()+
           '/servers/' +
           self.context.name +
           '/register?')
        return url


        
