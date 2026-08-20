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
from zopache.remote.postalcodes.interfaces import IGDPRForm
from zopache.remote.postalcodes.person import Person
from zopache.ttw.interfaces import IInternalPrincipal
from zopache.pages.page  import Page
from dolmen.forms.ztk import InvariantsValidation

@form_component
@name ('gdpr')
@context(IInternalPrincipal)
class GDPR(BaseEditForm):
    dataValidators = [InvariantsValidation]
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
        postalContainerName = countryCode + "_" + postalCode
        postalContainerName = slugify (postalName)
        postalContainer = root.get(postalName)
        if not postalContainer:
            directory = root["world"]
            if directory == None:
               directory = Page()                
               root["world"] = directory
            postalContainer = PostalCountryCode(countryCode, countryPostalCode,
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
        if ((countryName == "") and (countryPostalCode == "")): 
           if person:
               del person.__parent__[person.__name__]
               principal.person = None
           view.submissionError += "You did not provide location information and "
           view.submissionError += "therefore are not listed. "
           return
           #???? message is the wrong variable name.

        #Only 1 data   
        if (countryCode == "") != (countryPostalCode == ""):
            raise HTTPBadRequest(self.request.url)
        

        # Data looks good, get or create the postal container.
        postalContainer = self.getPostalContainer(root, 
                                                  principal.countryCode,
                                                  principal.countryPostalCode,
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
