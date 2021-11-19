from dolmen.forms.base import Actions
from zopache.crud import actions as formactions
from zopache.crud.actions import AddByTitle
from zopache.crud.addbytitleactions import AddByTitleAndView
from zopache.crud.actions import AddByTitleToTreeAndView
from zopache.crud.forms import AddByTitleForm, AddByNameForm
from zopache.pages.addpage import BaseAdd
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import IPage, ILink, IAddLink
from zopache.pages.page import Link
from zopache.business.exists import Duplicate
from zopache.forms.urlvalidator import DuplicateURLValidator
from zopache.pages.htmlvalidator import HTMLValidator

class AnonymousBase(BaseAdd):
    subTitle = "All submissions are reviewed before becoming being publicly visible."
    allowAnonymous = True    

    def postAddProcess(self,view = None):
        if self.treeSecurity():
            self.new.webApproved = True
        else:
            self.new.webApproved = False
        self.new.postAddProcess (view = self)

class AddAnonymousPageByTitle(AnonymousBase, AddByTitleForm):
     pass
 
     def addUnauthorizedActions(self):    
        self.actions = Actions(
                  AddByTitleAndView("Add and View", self.factory),
                  formactions.Cancel("Cancel","Cancel"))

#THIS ONE SHOULD GET RETIRED, BUT IS STILL IN USE        
class AddAnonymousPage(AddAnonymousPageByTitle):
    pass

class AddAnonymousPageByName(AnonymousBase, AddByNameForm):
    dataValidators = [DuplicateURLValidator, HTMLValidator]
    def addUnauthorizedActions(self):    
        self.actions = Actions(
                  formactions.AddByName("Add and View", self.factory),
                  formactions.Cancel("Cancel","Cancel"))        
                
class AddToTree(object):

    def addAuthorizedActions(self):   
              actions = Actions(
              formactions.AddByTitleToTreeAndView("Add", self.factory),
              formactions.Cancel("Cancel"))
              self.actions= actions
              
    def addUnauthorizedActions(self):    
           self.actions = Actions(
                  AddByTitleToTreeAndView("Add and View", self.factory),
                  formactions.Cancel("Cancel","Cancel"))    


@view_component
@name('addLink')
@target(IView)
@context(IPage)
class AddLink(AddAnonymousPageByTitle):
    interface = IAddLink
    title = "Add a Link"
    subTitle = "Refering to a remote page."
    factory = Link
