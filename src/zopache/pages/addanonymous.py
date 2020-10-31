from dolmen.forms.base import Actions
from zopache.crud import actions as formactions
from zopache.crud.actions import AddByTitle
from zopache.pages.pageactions import AddAndView
from zopache.crud.actions import AddByTitleToTreeAndView
from zopache.pages.addpage import AddPageBase
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import IPage, ILink
from zopache.pages.page import Link

class AddAnonymousPage(AddPageBase):
    count = 0 
    layoutName = "UserMenu"
    subTitle = "All submissions are reviewed before becoming being publicly visible."
    allowAnonymous = True    
    actions = Actions()    

    def addUnauthorizedActions(self):    
           self.actions = Actions(
                  formactions.AddByTitle("Add and View", self.factory),
                  formactions.Cancel("Cancel","Cancel"))
                   
    def postAddProcess(self,view = None):
        if self.treeSecurity():
            self.new.webApproved = True
        else:
            self.new.webApproved = False        
        self.new.postAddProcess (view = self)
        self.notifyAdminsNewPage()

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
        
