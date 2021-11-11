from mastodon import Mastodon

baseURL = 'https://mastodon.social'

class BaseBot(object):
    SITE = "https://dev.pythonlinks.info/callback"
    #SITE = 'https://UncensoredNews.US/callback'
    SCOPES = ['read:accounts','write:media','write:statuses']

    def getProxy (self,accessToken,baseURL,code):
        siteRoot = self.getSiteRoot()
        return  Mastodon(
            access_token = accessToken,
            client_id = siteRoot.clientKey.strip(),
            client_secret = siteRoot.clientSecret.strip(),
            code = code,
            api_base_url = baseURL)

    def userProxy(self):
        return self.getProxy(self.getPrincipal().accessToken.strip(),
                             baseURL,
                             None)
  
    def oauthProxy(self):
        accessToken = self.getSiteRoot().accessToken
        return self.getProxy(accessToken, baseURL,None)
    
    #def callbackProxy(self, accessToken):
    #    return self.getProxy(accessToken,baseURL,None)

    def accountProxy(self,code):
        return self.getProxy(self.getPrincipal().accessToken.strip(),
                             baseURL,
                             code)
        
