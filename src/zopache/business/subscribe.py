# -*- coding: utf-8 -*-

from BTrees.OOBTree import OOBTree


from dolmen.view import  make_view_response
from dolmen.view import name, context, view_component
from cromlech.browser.exceptions import HTTPFound

from zopache.core.page  import  Page
from zopache.business.interfaces import IFollow
from zopache.business.ifollow import IFollow
from zopache.business.member import Member

from zopache.json.event import MembersBase

class HasMembers(MembersBase):
    hasMembers = True
    
    def getTitleForDomain(self,view):
        domain = view.getDomain()        
        if domain in self:
            return self[domain].title
        else:
            return self.title


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

#THE REST IS NO LONGER USED.  SO SAD    
    """
    def getTitle(self):
         if self.hidden:
            return "Hidden"
         return self.title

    def setTitle(self,title):
         self.title = title
         return self.title
    



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
@name('unSubscribe')
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
