from slugify import slugify

from zope.interface import implementer

from zopache.ttw.principalfolder import InternalPrincipal
from zopache.ttw.interfaces import IInternalPrincipal

class IAccount(IInternalPrincipal):
    pass

@implementer(IAccount)
class Account(InternalPrincipal):
    webClass = "MastodonAccount"
    userId = 0
    userName = ''
    displayName= ''
    serverName = ''
    title =''
    description = ''
    
    def slugifiedHandle(self):
        return slugify(self.userName)
    
    @property
    def userName(self):
        return self.userAccountDict['username']

    @property
    def id(self):
        return self.userAccountDict['id']

    @property
    def mastodonDomain(self):
        return self.userAccountDict['mastodonDomain']

    @property
    def displayName(self):
        return self.userAccountDict['displayname']    
    
    def getTitle(self):
        return '@' + self.userName + '@' + self.mastodonDomain

    def setTitle(self,value):
        pass

    title = property(getTitle,setTitle)
    
    def getEmail(self):
        return  self.userName + '@' + self.mastodonDomain.lower()

    def setEmail(self,value):
        pass

    email = property(getEmail,setEmail)

    def notifyUserNewUser(self):
        pass
