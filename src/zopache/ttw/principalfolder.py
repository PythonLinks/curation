#MAYBE TWO PEPOLE CAN HAVE THE SAME SLUGIFIED HANDLE
#M

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
from zope.schema import ValidationError
from zope.interface import implementer, Interface
from zope.password.interfaces import IPasswordManager
from zope.password.password import SSHAPasswordManager as PasswordManager

from dolmen.container import BTreeContainer
from cromlech.browser import getSession, setSession
from cromlech.security import unauthenticated_principal as anonymous

from zopache.core import Container
from zopache.crud.interfaces import IImutable, IContainer
from zopache.ttw.interfaces import IPrincipalFolder, IInternalPrincipal
from zopache.core import getPrincipalFolder, getRoot
from zopache.ttw.file import FileBase

class DuplicateIDError(ValidationError):
    pass

@implementer(IInternalPrincipal)
class InternalPrincipal(Container,FileBase):
    _handle  = ''
    _email = ''
    _password = ''
    title = "Your Profile"
    talkURL =""
    permissions = ['Vote']
    chatPermission = False
    newsPermission = False
    pugPermission = False
    pyodidePermission = False
    helpPermission = False
    hirePermission = False
    recruitPermission = False

    def __init__(self):
        self.creationTime=time.time()
        self.modificationTime=time.time()
        Container.__init__(self)
        FileBase.__init__(self)
        
    def logout(self,session=None):
        if session is None:
            session = getSession()
        if 'user' in session:
            session.clear()
            return True
        return False

        
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
                getPrincipalFolder(self).notifyEmailChanged(oldEmail,   self)
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
                getPrincipalFolder(self).notifyHandleChanged(oldHandle,  self)
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
    icon="ttwicons/Container.svg"
    def __init__(self):
        super(PrincipalFolder, self).__init__()
        self.idByEmail = OOBTree()
        self.idBySlugifiedHandle = OOBTree()        
        
    def getPrincipalByUserName(self,userName, default = anonymous):

            id = self.getIdByEmail(userName)
            if id == None:
                id = self.getIdByHandle(userName)
            if id != None:    
               principal = self.getPrincipalById(id)
               return principal
            return default
        
    def getPrincipalById(self,id):
        #return self[id]
        return getRoot(self)[id]
    
    def notifyEmailChanged(self, oldEmail,  principal):
        """Notify the Container about changed email or handle of a user.
        We need this, so that our two other trees can be kept up-to-date.
        """
        # A user with the new login already exists
        if principal._email in self.idByEmail:
            raise ValueError('That Email Address already taken!')
        if oldEmail in self.idByEmail:
            del self.idByEmail[oldEmail]
        self.idByEmail[principal.email] = principal.__name__

    def notifyHandleChanged(self,  oldHandle, principal):
        """Notify the Container about changed email or handle of a user.
        We need this, so that our two other trees can be kept up-to-date.
        """
        # A user with the new login already exists
        if slugify(principal._handle) in self.idBySlugifiedHandle:
            raise ValueError('That Handle is already taken!')        

        oldHandle = slugify (oldHandle)
        if oldHandle in self.idBySlugifiedHandle:
           del self.idBySlugifiedHandle[oldHandle]
           
        handle = slugify (principal.handle)
        self.idBySlugifiedHandle[handle] = principal.__name__  

    def registerUser(self,principal):
        #Editing Email or Handle resets them.
        #So no need to do anything. 
        pass

    #REALLY THIS IS DELETE USER    
    def unRegisterUser(self,principal):	
        del self.idByEmail[principal.email]
        del self.idBySlugifiedHandle[slugify(principal.handle)]
        root = getRoot(self)
        root.deleteItem(principal)
        return
    
    def authenticate(self, credentials):
        """Return principal info if credentials can be authenticated
        """
        if not ('email' in credentials and 'password' in credentials):
            return None
        userName = credentials['email']
        internal = self.getPrincipalByUserName(userName,default = None)
        if internal is None:            
            return None
        if not internal.checkPassword(credentials["password"]):
            return None
        session = getSession()
        session['user'] = internal.email
        return internal
    

    def loginUser(self,user):
        session = getSession()
        session['user'] =getattr(user,'email')

    def getIdByEmail(self, email):
        return self.idByEmail.get (email,None)

    def getIdByHandle(self, handle):
        aSlug = slugify(handle) 
        return self.idBySlugifiedHandle.get(aSlug,None)

"""

A partial test script for adding admin. 
from zopache.core import getRoot

root = getRoot(item)

for key in item.idByEmail.keys():     print (key)

for key in item.idBySlufifiedHandle.keys():     print (key)

item["5886196134148338085"].__name__
 item["5886196134148338085"].__name__
 
"""
