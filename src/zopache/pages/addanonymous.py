from dolmen.forms.base import Actions
from zopache.crud import actions as formactions
from zopache.crud import actions as formactions
from zopache.crud.actions import AddByTitle
from zopache.pages.pageactions import AddAndView
from zopache.crud.forms import AddByTitleToTree
from zopache.pages.addpage import AddPageVeryBase

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
