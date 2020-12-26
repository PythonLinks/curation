from zopache.pages.page import Page
from zopache.pages.interfaces import IPage
from zope.interface import implementer

@implementer(IProxyPage)
class ProxyPage (Page):

    def getRemotePageName(self):
        return "us-politics"

    def getRemotePage(self):
        siteRoot = self.getSiteRoot()
        remotePageName = self.getRemotePageName
        if remotePageName in siteRoot:
            return siteRoot[remotePageName]
        else:
            return None
        
    def __contains__(self, key):
        return (key in self._data  or 
                key in self.getRemotePage())

    def __getitem__(self, name):
        if BTreeContainer.__contains__(self,name):
           return  BTreeContainer.__getitem__(self,name)
        else:
           return self.getRemoePage()[name]
    
    def get(self,name,default=None):
      if name in self:
         return self[name]

      # IF ALL ELSE FAILS
      return default

    def values(self):
        yield Page.values(self)
        yield self.getRemotePage.values(self)
        
