from zopache.core.viewdecorators import *
from zopache.ttw.html import CkScripts
from zopache.ttw.html import AddCkHTML, AddAceHTML
from .interfaces import IPage
from zopache.pages.page import Page


@view_component
@name('addpage')
@title("Add Page")
@target(IView)
@permissions('AddContent')
@context(IPage)    
class AddPage(AddAceHTML):
    interface = IPage
    label="Add a Wiki Page"
    factory = Page
    
    def getSubTitle(self):
        return (
                "To " +  
                self.context.webClass +
                u' called: ' +
                self.context.getTitle()
               )
    
    # LET THE BRANCH CHOOSE THE NAME
    def chooseName(self,name,theObject):
        parentBranch=self.context.parentBranch()
        name=parentBranch.chooseName(name,theObject)
        return name


    
