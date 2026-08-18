# -*- coding: utf-8 -*-

from slugify import slugify

from cromlech.browser.exceptions import HTTPFound
from dolmen.forms.base import Actions
from dolmen.forms.base import Fields
from dolmen.forms.base import action, name, context, form_component
from cromlech.browser.exceptions import HTTPBadRequest

from zopache.crud import update as editActions
from zopache.crud.actions import Cancel
from zopache.crud.forms import BaseEditForm
from zopache.crud.utils import getFactoryFields, getAllFields
from zopache.remote.postalcodes.actions  import RegisterAction
from zopache.remote.postalcodes.interfaces import IGDPRForm
from zopache.forms.validators.gdpr import GDPRValidator
from zopache.forms.validators.postal import PostalValidator
from zopache.remote.postalcodes.person import Person
from zopache.ttw.interfaces import IInternalPrincipal

@form_component
@name ('gdpr')
@context(IInternalPrincipal)
class GDPR(BaseEditForm):
    dataValidators = [GDPRValidator,PostalValidator]        
    layoutName = "UserMenu"    
    fields = Fields(IGDPRForm)
    subTitle = ""
    allowAnonymous = False
        
    def acquireTitle(self):
       return 'GDPR Permissions'

    def newURL(self,new):
        root = self.getSiteRoot()
        newURL =   root.homePage + self.randomIndex() 
        raise HTTPFound(newURL)
    
    def addUnAuthorizedActions(self):
        self.addAuthorizedActions()

    def addAuthorizedActions(self):
        self.actions = Actions(editActions.Edit("Save","Save"),
                    editActions.Cancel("Cancel","Cancel"))
        
    def renderMenuBar(self,layout):
        return ""



    def getPostalContainer(self, root, countryCode,
                           postalCode, countryName, latitude, longitude):
        postalName = countryCode + "_" + postalCode
        postalName = slugify (postalName)
        postalContainer = root.get(postalName)
        if not postalContainer:
            directory = root["world"]
            postalContainer = PostalCountryCode(countryCode, postalCode,
                                                countryName,
                                                latitude,
                                                longitude)
            directory [postalContainer.__name__]= postalContainer
        return postalContainer
       
    def postProcess(self, view = None):
        principal = self.context
        postalCode = principal.postalCode
        countryCode = principal.countryCode
        countryName  = principal.countryName
        root = self.getSiteRoot()


        person = principal.get('person',None)
       
        #No Data
        if ((countryName == "") and (postalCode == "")): 
           if person:
               del person.__parent__[person.__name__]
               principal.person = None
           view.message = "You did not provide location information and "
           view.message += "therefore are not listed. "
           return
           #???? message is the wrong variable name.

        #Only 1 data   
        if (countryCode == "") != (postalCode == ""):
            raise HTTPBadRequest(self.request.url)
        

        # Data looks good, get or create the postal container.
        postalContainer = self.getPostalContainer(root, 
                                                  principal.countryCode,
                                                  principal.postalCode,
                                                  principal.countryName,
                                                  principal.latitude,
                                                  principal.longitude)
        
        # Address exists, create the person. 
        if person == None:
            person = Person(principal)
            principal.person = person
            postalContainer[person.__name__] = person
            
        #Postalcode was changed.                
        elif person.__parent__!= postalContainer:
            name = person.__name__    
            del person.__parent__ [name]
            postalContainer[person.__name__] = person
            
        del principal.countryCode
        del principal.latitude
        del principal.longitude
        newURL = view.secureShortURL(context= postalContainer)
        raise HTTPFound(newURL)
