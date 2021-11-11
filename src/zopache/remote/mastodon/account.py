from zopache.core import Container

class MastodonAccount(Container):
    webClass = "MastodonAccount"
    userId = 0
    userName = ''
    displayName= ''
    serverName = ''
    title =''
    description = ''
    
    def getTitle(self):
        return '@' + self.userName + '@' + self.domain

    def setTitle(self,value):
        pass

    title = property(getTitle,setTitle)
