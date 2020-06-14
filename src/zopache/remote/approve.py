
from zopache.core.viewdecorators import *
from zopache.remote.rss import IRSS
from cromlech.browser.exceptions import HTTPFound
from zopache.forms.interfaces import IApprove
from zope.schema import Text
from zopache.crud.forms import EditForm
from zopache.core.viewdecorators import *

from zope import schema

class IApprove(Interface):
    webApproved = schema.Bool(
        title = "Approved for publication on the web.",
        required = False,
        default = False)

from zopache.core.breadcrumbs import Breadcrumbs    
@form_component
@name ('approve')
@context(IRSS)
@permissions('Manage')
class Approve (EditForm,Breadcrumbs):
    title = 'Approve this feed?'
    subTitle = "RSS Links will be moved to the main directory. "
    interface = IApprove
    fields = Fields(IApprove)
    def newURL (self,baseURL):
        #if self.context.webApproved:
           return baseURL + "/manage"
       
    def postProcess(self, view = None):
        context = self.context    
        self.root = self.getSiteRoot()
        items =self.getremoteURLs().values()

        if context.webApproved == True:
            for item in items:
                self.publish(item)
                
        if context.webApproved == False:
            for item in items:
                self.retract(item)

    def publish(self,item):
        item.webApproved = True
        if hasattr(item,'category'):
           category = self.root[item.category]
           if category!= item.__parent__:
              self.moveTo(item,category)

    def retract(self,item):
        item.webApproved = False        
        rss = item.rss
        if rss != item.__parent__:
           self.moveTo(item,self.context)
           
    def moveTo(self,item,category):
              name = item.__name__
              del item.__parent__[name]
              category [name] = item
              item.__name__ = name          
