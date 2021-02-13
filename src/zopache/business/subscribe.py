# -*- coding: utf-8 -*-

from BTrees.OOBTree import OOBTree

from cromlech.security import Unauthorized
from dolmen.view import  make_view_response
from dolmen.view import name, context, view_component
from cromlech.security import unauthenticated_principal as anonymous
from cromlech.browser.exceptions import HTTPFound

from zopache.core.baseform import Form
from zopache.core.page  import  Page
from zopache.business.interfaces import IFollow
from zopache.ttw.mail import Notify
from zopache.business.ifollow import IFollow
from zopache.business.member import Member

class HasMembers(object):
    hasMembers = True

    def getMembers(self):
         if not hasattr(self,'_members'):
            self._members =  OOBTree()
         return self._members
     
    members = property(getMembers) 
    
    def hasSubscribed (self,view):
        return self.isMemberA(view,'subscriber')
    
    def hasVolunteered (self,view):
        return self.isMemberA(view,'volunteer')
    
    def hasEndorsed (self,view):
        return self.isMemberA(view,'endorser')

    def mayDonate (self,view):
        return self.isMemberA(view,'donor')    

    def isMemberA(self,view,attribute):
         principal = view.request.principal
         if principal == anonymous:
            return False
         principalId = principal.__name__
         theMember = self.getOneMember(principalId)
         return getattr(theMember,attribute,False)
     
    def getOneMember(self,name):
        members = self.members
        if name in members:
           theMember = members[name] 
           if theMember.__class__ == Member:
               return theMember
        else:
              theMember = Member (name)   
              members [name] = theMember
              return theMember
    
    def isMember(self,view):
        if not view.isAuthenticated():
           return False
        if not hasattr(self,'members'):
           return False
        members = self.members
        name = view.request.principal.__name__
        if name in members:
            return True
        return False
    
    def hasFutureEvent(self):
        total = 0
        try:
           if self.candidateInfo["eventsPageURL"] != "":
              if self.candidateInfo["hasScheduledEvents"]:
                total +=  1
        except:
            pass
        total += len(self.listFutureEvents())
        return total
        
    

    def getTitle(self):
         if self.hidden:
            return "Hidden"
         return self.title

    def setTitle(self,title):
         self.title = title
         return self.title
     
    
class MemberForms(Form,Notify):
    
    def getOneMember(self,name):
        members = self.members
        if name in members:
           theMember = members[name] 
           if not theMember.__class__ == Member:
              theMember = Member (name)   
              members [name] = theMember
           return theMember

    def setMember(self,theMember):
        self.context.members[theMember.__name__] = theMember
        
         
class Connect(MemberForms):
    def update(self):
         principal = self.request.principal
         if principal == anonymous:
            return
        
         principalId = principal.__name__
         theMember = self.context.getOneMember(principalId)
         self.updateMember(theMember)
         self.setMember(theMember)         
         principal.addGroup (self.context.__name__)
         principal._p_changed = True
         self.notifyAdminsMembershipEvent(self.subject)
         raise HTTPFound(location=".")

class Disconnect(MemberForms):
    def update(self):
         principal = self.request.principal
         if principal == anonymous:
            return 
         principalId = principal.__name__
         members = self.context.members
         theMember = self.context.getOneMember(principalId)
         self.updateMember(theMember)
         if not theMember.isActive():
            del self.context.members [principalId] 
            principal.removeGroup (self.context.__name__)
         principal._p_changed = True
         self.setMember(theMember)
         self.notifyAdminsMembershipEvent(self.subject)
         raise HTTPFound(location=".")                  

#Volunteer     
@view_component
@name('volunteer')
@context(IFollow)
class volunteer(Connect):
    subject = "New Volunteer "
    
    def updateMember(self,member):
       member.volunteer = True
    
@view_component
@name('unvolunteer')
@context(IFollow)
class UnVolunteer(Disconnect):
    subject = "Volunteer Resigned "         
    
    def updateMember(self,member):
       member.volunteer = False

#SUBSCRIBE
@view_component
@name('subscribe')
@context(IFollow)
class Subscribe(Connect):
    subject = "New Subscriber "    
    def updateMember(self,member):
        member.subscriber = True
    
@view_component
@name('unsubscribe')
@context(IFollow)
class Unsubscribe(Disconnect):
    subject = "Subscriber Resigned "
    def updateMember(self,member):

       member.subscriber = False    

#Donate
@view_component
@name('donate')
@context(IFollow)
class Donate(Connect):
    subject = "New Donor "    
    def updateMember(self,member):
       member.donor = True
    
@view_component
@name('undonate')
@context(IFollow)
class Undonate(Disconnect):
    subject = "Donor Resigned "
    def updateMember(self,member):
       member.donor = False
     
#ENDORSE    
@view_component
@name('endorse')
@context(IFollow)
class Endorse(Connect):
    subject = "New Endorsement "    
    def updateMember(self,member):
       member.endorser = True
    
@view_component
@name('unendorse')
@context(IFollow)
class Unendorse(Disconnect):
    subject = "Endorser Resigned "
    def updateMember(self,member):
        member.endorser = False
      

"""        
#NOT USED    
@view_component
@name('cms-resign')
@context(IFollow)
class CMSResign(Resign):    
    make_response = make_view_response

@view_component
@name('cms-volunteer')
@context(IFollow)
class CMSFollow(Follow):     
    make_response = make_view_response     
"""
