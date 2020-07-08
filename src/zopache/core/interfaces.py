from zope.interface import Interface

class ITreeSecurity(Interface):
    pass

class IUserSecurity(Interface):
    pass

class ICountable(Interface):
      pass

class IVideo (ICountable):
     pass 
