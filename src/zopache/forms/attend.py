from cromlech.security import unauthenticated_principal as anonymous
from cromlech.security import Unauthorized
from dolmen.view import name, context, view_component
from cromlech.browser.exceptions import HTTPFound

from zopache.core.baseform import Form
from zopache.ttw.mail import Notify    
from zopache.json.interfaces import IJSONEvent


class MemberForms(Form, Notify):
    def __init__(self,context,request):
        Form.__init__(self,context,request)
        Notify.__init__(self)
    
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
         self.notifyAdminsMembershipEvent(self.subject)
         raise HTTPFound(location=".")

class Disconnect(MemberForms):
    def update(self):
         principal = self.request.principal
         if principal == anonymous:
            return 
         principalId = principal.__name__
         del self.context._members [principalId] 
         principal.removeGroup (self.context.__name__)
         self.notifyAdminsMembershipEvent(self.subject)
         raise HTTPFound(location=".")                  


#Attend An Event
@view_component
@name('attend')
@context(IJSONEvent)
class Attend(Connect):
    subject = "Attend "
    def updateMember(self,member):
       member.attend = True

#Cancel Attendance       
@view_component
@name('cancel')
@context(IJSONEvent)
class Cancel(Disconnect):
    subject = "Cancel Attendance "         
    
    def updateMember(self,member):
       member.attend = False     
