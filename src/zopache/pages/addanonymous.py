from dolmen.forms.base import Actions
from zopache.crud import actions as formactions
from zopache.crud import actions as formactions
from zopache.crud.actions import AddByTitle
from zopache.pages.pageactions import AddAndView
from zopache.crud.forms import AddByTitleToTree
from zopache.pages.addpage import AddPageVeryBase
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import IPage, ILink
from zopache.pages.page import Link

class AddToTreeAndView(AddByTitleToTree):
    def newURL(self,baseURL):
        return baseURL 

class AddAnonymous(AddPageVeryBase):
    count = 0 
    layoutName = "UserMenu"
    subTitle = "All submissions are reviewed before becoming being publicly visible."
    allowAnonymous = True    
    actions = Actions()    
    def update(self):
        if self.treeSecurity():
           self.addAuthorizedActions()
        else:
           self.addUnauthorizedActions()    

    def addUnauthorizedActions(self):    
           self.actions = Actions(
                  AddAndView("Add and View", self.factory),
                  formactions.Cancel("Cancel","Cancel"))
                   
    def postAddProcess(self,view = None):
        if self.treeSecurity():
            self.new.webApproved = True
        else:
            self.webApproved = False        
        self.new.postAddProcess (view = self)
        self.notifyAdminsNewPage()

    def widgetJsonURL(self):
        siteRoot = self.getSiteRoot()
        mapName = siteRoot.mapName
        uri ="https://" + self.getDomain() + "/" + mapName + "/json"
        return uri
        

class AddAnonymousToTree(AddAnonymous):
    def update(self):
        self.actions = Actions(
                  AddToTreeAndView("Add and View", self.factory),
                  formactions.Cancel("Cancel","Cancel"))

#ADD LINK
from zopache.pages.page import Link
from zopache.pages.interfaces import ILink
@view_component
@name('addLink')
@target(IView)
@context(IPage)
class AddLink(AddAnonymous):
    interface = ILink
    title = "Add a Link"
    subtitle = "To a remote web page."
    factory = Link
    
        
