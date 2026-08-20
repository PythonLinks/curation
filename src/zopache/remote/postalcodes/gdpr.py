# -*- coding: utf-8 -*-

from slugify import slugify

from cromlech.security import Unauthorized
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
from zopache.remote.postalcodes.countrypostalcode import CountryPostalCode
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

    def update(self):
        if not (self.request.principal == self.context):
            raise Unauthorized ("People can only update their own data.")
        BaseEditForm.update(self)
        
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
        postalContainerName = slugify (postalContainerName)
        postalContainer = root.get(postalContainerName)
        if not postalContainer:
            directory = root["world"]
            if directory == None:
               directory = Page()                
               root["world"] = directory
            postalContainer = CountryPostalCode(countryCode, postalCode,
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
        principalFolder = self.getPrincipalFolder()

        #No Data - principal belongs in /root/person
        if ((countryName == "") and (postalCode == "")):
           if principal.__parent__ is not principalFolder:
               name = principal.__name__
               del principal.__parent__[name]
               principalFolder[name] = principal
           view.submissionError += "You did not provide location information and "
           view.submissionError += "therefore are not listed. "
           return

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

        # Move the principal itself into the postal container.
        if principal.__parent__ is not postalContainer:
            name = principal.__name__
            if principal.__parent__ is principalFolder:
                principalFolder.removeItem(principal)
            else:
                del principal.__parent__[name]
            postalContainer[name] = principal

        del principal.countryCode
        del principal.latitude
        del principal.longitude
        newURL = view.secureShortURL(context= postalContainer)
        raise HTTPFound(newURL)
