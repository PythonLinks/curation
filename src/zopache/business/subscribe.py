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

class HasMembers(object):
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

    
class MemberForms(Notify):

    def getAllMembers(self):
         context = self.context
         if not hasattr(contect,'members'):
            context.Members =  OOBTree()
         return context.members
     
    def getOneMember(self,name):
        members = self.members
        if name in members:
           theMember = member[name] 
           if theMember.__class__ == Member:
               return theMember
           else:
              theMember = Member [name]   
              members [name] = theMember
              return TheMember

    def setMember(self,theMember):
        self.members[theMember.__name__] = theMember
        
class Connect(MemberForms):
    def update(self):
         principal = self.request.principal
         if principal == anonymous:
            return
        
         principalId = principal.__name__
         theMember = self.getOneMember(principalId)
         self.updateMember(theMember)
         self.setMember(theMember)         
         principal.groups.add (self.context.__name__)
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
         theMember = self.getOneMember(principalId)
         self.updateMember(theMember)
         if not theMember.isActive():
            del self.context.members [principalId] 
            principal.groups.remove (self.context.__name__)
         principal._p_changed = True
         self.setMember(theMember)
         self.notifyAdminsMemberEvent(self.subject)
         raise HTTPFound(location=".")                  

#Volunteer     
@view_component
@name('volunteer')
@context(IFollow)
class volunteer(Connect):
    subject = "New Volunteer "
    
    def updateMember(member):
       member.volunteer = True
    
@view_component
@name('unvolunteer')
@context(IFollow)
class UnVolunteer(Disconnect):
    subject = "Volunteer Resigned "         
    
    def updateMember(member):
       member.volunteer = False

#SUBSCRIBE
@view_component
@name('subscribe')
@context(IFollow)
class Subscribe(Connect):
    subject = "New Subscriber "    
    def updateMember(member):
       member.subscriber = True
    
@view_component
@name('unsubscribe')
@context(IFollow)
class Unsubscribe(Disconnect):
    subject = "Subscriber Resigned "
    def updateMember(member):
       member.subscriber = False    

#Donate
@view_component
@name('donate')
@context(IFollow)
class Donate(Connect):
    subject = "New Donor "    
    def updateMember(member):
       member.donor = True
    
@view_component
@name('undonate')
@context(IFollow)
class Undonate(Disconnect):
    subject = "Donor Resigned "
    def updateMember(member):
       member.donor = False
     
#ENDORSE    
@view_component
@name('endorse')
@context(IFollow)
class Endorse(Connect):
    subject = "New Endorsement "    
    def updateMember(member):
       member.endorse = True
    
@view_component
@name('unendorse')
@context(IFollow)
class Unendorse(Disconnect):
    subject = "Endorser Resigned "
    def updateMember(member):
        member.endorse = False
      

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
