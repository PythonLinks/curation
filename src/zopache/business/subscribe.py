# -*- coding: utf-8 -*-

from BTrees.OOBTree import OOBTree

from cromlech.browser.exceptions import HTTPFound
from cromlech.security import Unauthorized
from dolmen.view import name, context, view_component
from cromlech.security import unauthenticated_principal as anonymous
from zopache.core.page  import  Page
from zopache.business.interfaces import IOrganization

class BaseMembers(Page):
    def addVariables (self):    
         if not hasattr(self.context,'members'):
             self.context.members = OOBTree()
         principal = self.request.principal
         if not hasattr(principal,'groups'):
              principal.groups = set()
              
    
@view_component
@name('join')
@context(IOrganization)
class Join(BaseMembers):
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
@name('leave')
@context(IOrganization)
class Leave(BaseMembers):
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

    


