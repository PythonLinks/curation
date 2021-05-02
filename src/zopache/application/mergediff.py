from zope.interface import Interface

from zopache.core.viewdecorators import *
from zopache.core.breadcrumbs import Breadcrumbs
from zopache.core.view import LayoutView
from zopache.ttw.interfaces import IAceEdit

@view_component
@target(IView)
@name ('diff')
@context(Interface)
class Diff (LayoutView,Breadcrumbs):

    title = "Compare two different branches."
    subTitle = "Basically a graphical diff."
    
    def update(self):
        self.template = self.getTemplates()['Diff']['form']
        
    def breadcrumbs(self,item = None):
        if item == None:
            item = self.context
        return self.breadcrumbsView(item,viewName='diff',showTitles=False)

from zopache.ttw.htmlviews import Index
@view_component
@target(IView)
@name ('acediff')
@context(IAceEdit)
class AceDiff (LayoutView,Breadcrumbs):
    title = "Merge Two Different Ace Objects."
    subTitle = "Basically a graphical merge."
    
    def update(self):
        self.template = self.getTemplates()['AceDiff']['form']
    
    def breadcrumbs(self,item = None):
        if item == None:
            item = self.context
        return self.breadcrumbsView(item,viewName='diff',showTitles=False)    
    
