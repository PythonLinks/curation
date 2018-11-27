
from zope.cachedescriptors.property import CachedProperty
from dolmen.forms.base import Actions
from zopache.pages.pageactions import *
from zopache.crud import actions as formactions
from zopache.pages.pageactions import *
from zopache.core.viewdecorators import *
from zopache.ttw.html import CkScripts
from zopache.ttw.html import AddCkHTMLBase
from .interfaces import IPage
from zopache.pages.page import Page
from zopache.core.uniquename import UniqueName
from zopache.crud.forms import AddByTitleForm

class AddPageBase(AddCkHTMLBase,AddByTitleForm,UniqueName):
    def getSubTitle(self):
        return (
                "To " +  
                self.context.webClass +
                u' called: ' +
                self.context.getTitle()
               )

    @CachedProperty
    def actions(self):
        return Actions(
              AddAndView("Add and View", self.factory),
              AddAndCkEdit("Add and ckEdit", self.factory),
              AddAndAceEdit("Add and AceEdit", self.factory),
              formactions.Cancel("Cancel","Cancel"))
    

    
@view_component
@name('addpage')
@title("Add Page")
@target(IView)
@permissions('AddContent')
@context(IPage)    
class AddPage(AddPageBase):
    interface = IPage
    label="Add a Wiki Page"
    factory = Page
    


    
