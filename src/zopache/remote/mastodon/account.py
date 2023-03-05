from slugify import slugify

from zope.interface import implementer

from zopache.ttw.principalfolder import InternalPrincipal

from zopache.remote.mastodon.interfaces import IAccount

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
    
import crom
from zopache.zmi.interfaces import IURLSegment
@crom.adapter
@crom.sources(IAccount)
@crom.target(IURLSegment)
class IRemoteAccountAdaptor(object):
    def __init__(self,context):
        self.context=context   

    def getSegment(self):
        return 'permissions'
