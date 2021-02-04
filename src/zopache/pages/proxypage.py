from zopache.pages.page import Page
from zopache.pages.interfaces import IPage, IProxyPage


from zope.interface import implementer

#@implementer(IProxyPage)
class ProxyPage (Page):

    def getRemotePageName(self):
        #return "us-politics"
        return "biden-administration"
    def getRemotePage(self):
        siteRoot = self.getSiteRoot()
        remotePageName = self.getRemotePageName()
        if remotePageName in siteRoot:
            return siteRoot[remotePageName]
        else:
            return None
        
    def __contains__(self, key):
        return (key in self._data  or 
                key == self.getRemotePageName())

    def __getitem__(self, name):
        if Page.__contains__(self,name):
           return  Page.__getitem__(self,name)
        elif name == self.getRemotePageName():            
           return self.getRemotePage()
        else:
           raise Exception(f"""Cannot Find an object called "{name}" """) 
    
    def get(self,name,default=None):
        try:
           return self.__get__item(name)
        except:
           return default

    def childCategories(self):
        return (Page.childCategories(self) +
              [self.getRemotePage()])
        
