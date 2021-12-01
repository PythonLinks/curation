from zope.interface import Interface
from cromlech.browser.interfaces import IPublicationRoot

class ITreeSecurity(Interface):
    pass

class IUserSecurity(Interface):
    pass

class ICountable(Interface):
      pass

#Anything that can be published is IPublicationRoot
#This is for the tops of websites, 1 below the root. 
class ISiteRoot(IPublicationRoot):
    pass
