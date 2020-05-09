# -*- coding: utf-8 -*-

from BTrees.OOBTree import OOBTree

from cromlech.browser.exceptions import HTTPFound
from cromlech.security import Unauthorized
from dolmen.view import name, context, view_component
from cromlech.security import unauthenticated_principal as anonymous
from zopache.core.page  import  Page
from zopache.business.interfaces import IFollow
from dolmen.view import  make_view_response

class Member(object):
    def __init__ (self):
        self.members = OOBTree()
        
    def isMember(self,view):
        if not view.isAuthenticated():
           return False
        if not hasattr(self,'members'):
           return False
        name = view.request.principal.__name__
        if name in self.members:
            return True
        return False
    
    
class BaseMembers(Page):
    def addVariables (self):    
         if not hasattr(self.context,'members'):
             self.context.members = OOBTree()
         principal = self.request.principal
         if not hasattr(principal,'groups'):
              principal.groups = set()
              
    
@view_component
@name('follow')
@context(IFollow)
class Follow(BaseMembers):
    def update(self):
         principal = self.request.principal
         
         if principal == anonymous:
            return
        
         self.addVariables()

         principalId = principal.__name__        
         self.context.members [principalId] = principalId
         principal.groups.add (self.context.__name__)
         principal._p_changed = True
         raise HTTPFound(location=".")

@view_component
@name('cms-follow')
@context(IFollow)
class CMSFollow(BaseMembers):     
    make_response = make_view_response     

@view_component
@name('unfollow')
@context(IFollow)
class UnFollow(BaseMembers):
    def update(self):
         principal = self.request.principal

         if principal == anonymous:
            return 
         self.addVariables()       
         principalId = principal.__name__                
         del self.context.members [principalId] 
         principal.groups.remove (self.context.__name__)
         principal._p_changed = True         
         raise HTTPFound(location=".")                  

@view_component
@name('cms-unfollow')
@context(IFollow)
class CMSUnFollow(UnFollow):    
    make_response = make_view_response

