# -*- coding: utf-8 -*-

from BTrees.OOBTree import OOBTree

from cromlech.security import Unauthorized
from dolmen.view import  make_view_response
from dolmen.view import name, context, view_component
from cromlech.security import unauthenticated_principal as anonymous
from cromlech.browser.exceptions import HTTPFound

from zopache.core.page  import  Page
from zopache.business.interfaces import IFollow
from zopache.ttw.mail import Notify
from zopache.business.ifollow import IFollow

class Member(object):
    eventsPageURL = ""
    hasScheduledEvents = False
    
    def __init__ (self):
        self.members = OOBTree()

    def hasFutureEvent(self):
        if self.eventsPageURL != "":
           if self.hasScheduledEvents:
               return 1
        return 0  
        
    def isMember(self,view):
        if not view.isAuthenticated():
           return False
        if not hasattr(self,'members'):
           return False
        name = view.request.principal.__name__
        if name in self.members:
            return True
        return False

    def getMembers(self,view):
        if not hasattr(self,'members'):
           return {}
        return self.members
    
    
class BaseMembers(Page):
    def addVariables (self):    
         if not hasattr(self.context,'members'):
             self.context.members = OOBTree()
         principal = self.request.principal
         if not hasattr(principal,'groups'):
              principal.groups = set()
              
    
@view_component
@name('volunteer')
@context(IFollow)
class Follow(BaseMembers,Notify):
    def update(self):
         principal = self.request.principal
         
         if principal == anonymous:
            return
        
         self.addVariables()

         principalId = principal.__name__        
         self.context.members [principalId] = principalId
         principal.groups.add (self.context.__name__)
         principal._p_changed = True
         self.notifyAdminsNewVolunteer()
         raise HTTPFound(location=".")

@view_component
@name('cms-volunteer')
@context(IFollow)
class CMSFollow(Follow):     
    make_response = make_view_response     

@view_component
@name('resign')
@context(IFollow)
class Resign(BaseMembers,Notify):
    def update(self):
         principal = self.request.principal
         if principal == anonymous:
            return 
         self.addVariables()       
         principalId = principal.__name__                
         del self.context.members [principalId] 
         principal.groups.remove (self.context.__name__)
         principal._p_changed = True         
         self.notifyAdminsVolunteerResigned()
         raise HTTPFound(location=".")                  

@view_component
@name('cms-resign')
@context(IFollow)
class CMSResign(Resign):    
    make_response = make_view_response

