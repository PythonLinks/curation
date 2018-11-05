

# Copyright (c) 2004 Zope Foundation and Contributors.
#Copyright Chrisotpher Lozinski 2018
# All Rights Reserved.

# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).
#And to the CV License agreement. 


# THIS File WAS EXTRACTED FROM zope.pluggableauth
# AND SIMPLIFIED
from slugify import slugify
import time
from BTrees.OOBTree import OOBTree
from zope.interface import implementer, Interface
from zope.password.interfaces import IPasswordManager
from zope.password.password import SSHAPasswordManager as PasswordManager
from dolmen.container import BTreeContainer
from cromlech.browser import getSession

from zopache.core import Container
from zopache.crud.interfaces import IImutable, IContainer
from .interfaces import IPrincipalFolder, IInternalPrincipal

class DuplicateIDError(KeyError):
    pass




@implementer(IInternalPrincipal,IContainer)
class InternalPrincipal(Container):
    _handle  = ''
    _email = ''
    _password = ''
    title = "Your Profile"
    def __init__(self):
        self.creationTime=time.time()
        self.modificationTime=time.time()
        Container.__init__(self)
                         
    """ Pricipals which are stored in the ZODB Principal Folder"""
    def upVote(self,item):
        self.possiblyCreateVoteCounts()
        key = item.__name__
        if key in self._downVotes:
            del self._downVotes[key]
        if key in self._upVotes:
            del self._upVotes[key]            
            return
        self._upVotes[key] = time.time()
        self._p_changed = True
   
    def downVote(self,item):
        self.possiblyCreateVoteCounts()
        key = item.__name__
        if key in self._upVotes:
            del self._upVotes[key]
        if key in self._downVotes:
           del self._downVotes[key]            
           return
        self._downVotes[key] = time.time()           
        self._p_changed = True
        
            
    def possiblyCreateVoteCounts(self):    
        if not hasattr(self,"_upVotes"):
           self._upVotes = {}
        if not hasattr(self,"_downVotes"):
           self._downVotes = {}

           
    def getTitle(self):
        return self._handle

    def getId(self):
        return self._email    
    
    
    def getPassword(self):
        return self._password

    def setPassword(self, password):
        self._password = PasswordManager().encodePassword(password,salt='')


    def checkPassword(self, password):
        return PasswordManager().checkPassword(self.password, password)

    def getEmail(self):
        return self._email


    def getHandle(self):
        return self._handle

        
    def setEmail(self, email):
        oldEmail = self._email
        if email == oldEmail:
           return
        self._email = email
        if self.__parent__ is not None:
            try:
                self.__parent__.notifyEmailChanged(oldEmail,   self)
            except ValueError:
                self._email = oldEmail
                raise


    def setHandle(self, handle):
        oldHandle = self._handle
        if handle == oldHandle:
            return
        self._handle = handle
        if self.__parent__ is not None:
            try:
                self.__parent__.notifyHandleChanged(oldHandle,  self)
            except ValueError:
                self._handle = oldHandle
                raise
            
    password = property(getPassword, setPassword)
    title = property(getTitle)
    email = property(getEmail, setEmail)
    id = property(getId)
    handle = property(getHandle, setHandle)    

            
@implementer(IPrincipalFolder,IImutable)
class PrincipalFolder(Container):
    """ A Container of Principals.
    """

    def __init__(self):
        super(PrincipalFolder, self).__init__()
        self.idByEmail = OOBTree()
        self.idBySlugifiedHandle = OOBTree()        
        
        
    def notifyEmailChanged(self, oldEmail,  principal):
        """Notify the Container about changed email or handle of a user.
        We need this, so that our two other trees can be kept up-to-date.
        """
        
        # A user with the new login already exists
        if principal._email in self.idByEmail:
            raise ValueError('That Email Address already taken!')
        
        del self.idByEmail[oldEmail]
        self.idByEmail[principal.email] = principal.__name__



    def notifyHandleChanged(self,  oldHandle, principal):
        """Notify the Container about changed email or handle of a user.
        We need this, so that our two other trees can be kept up-to-date.
        """
        # A user with the new login already exists
        if slugify(principal._handle) in self.idBySlugifiedHandle:
            raise ValueError('That Handle is already taken!')        

        del self.idBySlugifiedHandle[slugify(oldHandle)]
        self.idBySlugifiedHandle[slugify(principal.handle)] = principal.__name__        
    def __setitem__(self, id, principal):
        """Add a user """

        # A user with the new login or handle  already exists
        if principal.email in self.idByEmail:
            raise DuplicateIDError('That Email address is already taken!')

        if slugify(principal.handle) in self.idBySlugifiedHandle:
            raise DuplicateIDError('That Handle is already taken!')        

        super(PrincipalFolder, self).__setitem__(id, principal)
        self.idByEmail[principal.email] = id
        self.idBySlugifiedHandle[slugify(principal.handle)] = id        

    def __delitem__(self, id):
        """Remove principal information."""
        principal = self[id]
        super(PrincipalFolder, self).__delitem__(id)
        del self.idByEmail[principal.email]
        del self.idBySlugifiedHandle[slugify(principal.handle)]        

    def authenticate(self, credentials):
        """Return principal info if credentials can be authenticated
        """
        import pdb; pdb.set_trace()
        if not ('email' in credentials and 'password' in credentials):
            return None
        id = self.idByEmail.get(credentials['email'])
        if id is None:
            id = self.idBySlugifiedHandle.get(
                 slugify(credentials['email']))            
        if id is None:            
            return None
        internal = self[id]
        if not internal.checkPassword(credentials["password"]):
            return None
        session = getSession()
        session['user'] = credentials['email']
        return internal

    def loginUser(self,user):
        session = getSession()
        session['user'] =getattr(user,'email')

    def getIdByEmail(self, email):
        return self.idByEmail[email]

    def getIdByHandle(self, handle):
        return self.idBySlugifiedHandle[slugiy(handle)]    

