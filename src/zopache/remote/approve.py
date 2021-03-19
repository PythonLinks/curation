from zope import schema

from zopache.core.viewdecorators import *
from zopache.remote.rssarticle import IRSSArticle
from cromlech.browser.exceptions import HTTPFound
from zopache.forms.interfaces import IApprove
from zope.schema import Text
from zopache.crud.forms import EditForm
from zopache.core.viewdecorators import *
from zopache.ttw.treewidget import TreeField


class IApprove(Interface):
    title = schema.TextLine(
        title = u'Page Name',
        description = u'Describe this page.',
        required = True,
    )

    description= schema.Text(
        title = 'Description',
        description = """A brief introduction of this page.  
                        This is used by the search functions.""",
        required = False,
        default = u'',
    )        
    webApproved = schema.Bool(
        title = "Visible or not?",
        description = "Use this option to hide this article.",
        required = False,
        default = False)

    publicationApproved = schema.Bool(
        title =  "Published or not?",
        description = "Move to its category, or back to its RSS feed.",
        required = False,
        default = False)    

    category=TreeField(
           title="Category Search",
           description= """Choose where to move the articcle. """,
           required = False,
            )
    
from zopache.core.breadcrumbs import Breadcrumbs    
@form_component
@name ('approve')
@context(IRSSArticle)
@permissions('Manage')
class Approve (EditForm,Breadcrumbs):
    title = 'Approve this Article?'
    subTitle = "The article will be moved to its new location. "
    interface = IApprove
    fields = Fields(IApprove)
    def newURL (self,baseURL):
           return baseURL 
       
    def postProcess(self, view = None):
        self.siteRoot = self.getSiteRoot()
        context = self.context

        if context.publicationApproved == True:
           if context.category !="": 
                self.publish()
                context.addImage()
        else:
           self.retract()
        
    def publish(self):
        context = self.context
        if hasattr(context,'category'):
           if context.category != "":
              category = self.siteRoot[context.category]
              if category!= context.__parent__:
                self.context.moveTo(category)

    def retract(self):
        rssFeed = self.context.rssFeed
        if rssFeed != self.__parent__:
           self.context.moveTo(rssFeed)
           


