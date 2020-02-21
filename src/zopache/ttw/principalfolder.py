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
from zopache.core.getroot import getPrincipalFolder, getSiteRoot, getProducts
from zopache.ttw.file import FileBase

class DuplicateIDError(ValidationError):
    pass

from zopache.pages.page import Page


@implementer(IInternalPrincipal)
class InternalPrincipal(FileBase,Page):
    _handle  = ''
    _email = ''
    _password = ''
    title = "Your Profile"
    talkURL =""
    title = ""
    source = ""
    description = ""
    permissions = ['Vote']
    chatPermission = False
    newsPermission = False
    pugPermission = False
    pyodidePermission = False
    helpPermission = False
    hirePermission = False
    recruitPermission = False
    contentType = "text/plain"
    webClass = 'Person'
    branchSize = 1
    
    """
    from persistent.list import PersistentList
    def makeOrdered(self):
        self._order = PersistentList()
        for item in self:
               self._order.append(item)
    """           
        
    def __init__(self):
        self.creationTime=time.time()
        self.modificationTime=time.time()
        Page.__init__(self)
        FileBase.__init__(self)

    def logout(self,session=None, view = None):
        if session is None:
            session = getSession()
        if 'user' in session:
            session.clear()
            return True
        return False

    def logout(self,session=None, view = None):
        if session is None:
            session = getSession()
            
        if 'user' in session:
            session.clear()



        
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

    def slugifiedHandle(self):
        return slugify(self.handle)
                 
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

    def postAddProcess (self, view =None):
        view.notifyUserNewUser()
        view.notifyAdminsNewUser()
            
    password = property(getPassword, setPassword)
    title = property(getTitle)
    email = property(getEmail, setEmail)
    id = property(getId)
    handle = property(getHandle, setHandle)    



def key(item):
    return item._p_mtime

@implementer(IPrincipalFolder)
class PrincipalFolder(Container):
    """ A Container of Principals.
    """
    title = "Principal Folder"
    description = "This is where the user details are stored. "
    branchSize = 1
    def html (self) :
        return ""
    icon="ttwicons/Container.svg"
    webClass = "PrincipalFolder"
    def __init__(self):
        super(PrincipalFolder, self).__init__()
        self.idByEmail = OOBTree()
        self.idBySlugifiedHandle = OOBTree()

    def convert (self):
        del self.idByEmail
        del self.idBySlugifiedHandle
        self.emailIndex= OOBTree()
        self.slugifiedHandleIndex = OOBTree()
        for item in self.values():
            self.emailIndex[item.email]= item
            self.slugifiedHandleIndex [item.slugifiedHandle()] = item
            
    def setJson(self):
        pass

    def values(self):
        all = []
        for item in Container.values(self):
            all.append(item)
        all.sort(key=key, reverse = True)
        return all
    
    def indexPeople(self):
        self.idByEmail = OOBTree()
        self.idBySlugifiedHandle = OOBTree()                
        for item in self.values():
          try:
            self.idByEmail[item.email] = item.__name__
            slug = item.slugifiedHandle()
            self.idBySlugifiedHandle[slug] = item.__name__
          except:
              pass
          
    def getPrincipalByUserName(self,userName, default = anonymous):

            id = self.getIdByEmail(userName)
            if id == None:
                id = self.getIdByHandle(userName)
            if id != None:    
               principal = self.getPrincipalById(id)
               return principal
            return default
        
    def getPrincipalById(self,id):
        return self[id]
        #result = getSiteRoot(self)[id]
        #return result
    
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
           
        handle = principal.slugifiedHandle()
        self.idBySlugifiedHandle[handle] = principal.__name__  

    def registerUser(self,principal):
        #Editing Email or Handle resets them.
        #So no need to do anything. 
        pass

    #REALLY THIS IS DELETE USER    
    def unRegisterUser(self,principal):	
        del self.idByEmail[principal.email]
        del self.idBySlugifiedHandle[principal.slugifiedHandle()]
        root = getSiteRoot(self)
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

    #USED BY REGISTER VALIDATORS
    def existsHandle(self,handle):           
        aSlug = slugify(handle) 
        return aSlug in self.idBySlugifiedHandle            
