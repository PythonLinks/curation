import crom
from zope import schema
from zope import interface
from cromlech.container.interfaces import IBTreeContainer
from zopache.zmi.contents import Contents
try: 
    from zopache.core.page  import  Page
except ImportError:
    from cromdemo.browser import Page
from . import tal_template
from crom import target, order
from dolmen.view import name, context, view_component
from cromlech.browser.directives import title
from dolmen.container import IBTreeContainer
from cromdemo.interfaces import ITab
from .contents import Contents
from cromlech.security import permissions
from zopache.zmi.interfaces import IURLSegment

@view_component
@name('manage')
@title("Manage")
@target(ITab)
@permissions('Manage')
@context(IBTreeContainer)
class Manage(Page,Contents):
    label=''
    subTitle='Manage Container'
    template = tal_template('zmi.pt')

    def getManageURL(self,item):
        url = self.url(item)
        segment =  IURLSegment(item).getSegment()
        return url + '/' + segment
                
    def breadcrumbs(self):
        return self.breadcrumbsManage()

    def iconTag(self,url):
        return """ <img height="17px" width="17px" src="%s"> </img>""" % url
 
    def iconHTML(self,item):
        if (hasattr(item,'icon') and
           item.icon!=''):
           return self.iconTag("/fanstatic/"+item.icon) 
        else:
           return ''
       
#USED TO FIRE UP A DEBUGGER TO MAKE MANUAL CHANGES    
@view_component
@name('fix')
@title("Fix")
@target(ITab)
@permissions('Manage')
@context(IBTreeContainer)
class Fix(Manage):

       def update(self):
          item=self.context
          import pdb; pdb.set_trace()


          from zopache.categories.data.readConference.importData import importData
          #importData(item)
          
          fred = 1







       

       



