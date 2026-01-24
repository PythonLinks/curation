
# -*- coding: utf-8 valida-*-

#This software is subject to the CV and Zope Public Licenses.
from dolmen.forms.base import Actions
from dolmen.forms.base import Fields
from dolmen.forms.base import action, name, context, form_component

from zopache.crud.forms import BaseEditForm
from zopache.crud.actions import Cancel
from zopache.forms.validators.gdpr import GDPRValidator
from zopache.crud import update as editActions
from zopache.forms.interfaces import IGDPRForm
from zopache.ttw.interfaces import IInternalPrincipal

@form_component
@name ('gdpr')
@context(IInternalPrincipal)
class GDPR(BaseEditForm):
    dataValidators = [GDPRValidator]
    layoutName = "UserMenu"    
    fields = Fields(IGDPRForm)
    subTitle='For the ASIC and FPGA Meetup'
    allowAnonymous = False
        
    def acquireTitle(self):
       return 'Register'

    def newURL(self,new):
        root = self.getSiteRoot()
        newURL =   root.homePage
        return newURL

    def addUnAuthorizedActions(self):
        self.addAuthorizedActions()

    def addAuthorizedActions(self):
        self.actions = Actions(editActions.Edit("Save","Save"),
                    editActions.Cancel("Cancel","Cancel"))
    def renderMenuBar(self,layout):
        return ""
        
"""
from zopache.forms.validators.postal import PostalValidator
from zopache.remote.postalcodes.postalcode import getPostalContainer
from zopache.remote.postalcodes.voter import Voter
from zopache.forms.adduseractions  import SubscribeAction
from zopache.forms.adduseractions  import RegisterAction

from zopache.crud.utils import getFactoryFields, getAllFields

from zopache.forms.interfaces import ISubscribe
   
From newURL()   
 #       postalCode = self.context.postalCode
 #       if postalCode:
 #           postalContainer = getPostalContainer(root,
 #                                            postalCode)            
 #           newURL = "/" + postalContainer.name
 #       else:

   #    The following is needed if we are mapping people. 
#    dataValidators = [GDPRValidator,PostalValidator]    

   
    def postProcess(self, view = None):
        #The self variables are needed later for newURL.
        principal = self.context
        self.principal = principal

        postalCode = principal.postalCode
        self.postalCode = postalCode
        voter = principal.voter
        root = self.getSiteRoot()
        self.root = root
        postalContainer = getPostalContainer(root,postalCode)
        self.postalContainer = postalContainer
        
        #No postal code and no voter, nothing to do.                 
        if not postalCode and (voter == None):
            return

        #User deleted postal code, but there is a voter.                 
        elif not postalCode and (voter != None):
           del voter.parent[voter.name]
           principal.voter = None

        # A new postalCode, create the voter        
        elif postalCode and (voter == None):
            voter = Voter(principal)
            newName = root.getUniqueNumberString()
            voter.__parent__ = postalContainer
            postalContainer[newName] = voter
            principal.voter = voter
            
        #Postalcode was changed.                
        elif voter.__parent__.__name__ != postalCode:
            name = voter.name    
            del voter.parent [name]
            voter.__parent__ = postalContainer
            postalContainer[name] = voter    
"""            
         
