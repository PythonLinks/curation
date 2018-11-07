import crom
from zope import schema
from zope import interface
from cromlech.container.interfaces import IBTreeContainer
from zopache.zmi.contents import Contents
from zopache.core.page  import  Page

from . import tal_template
from crom import target, order
from dolmen.view import name, context, view_component
from cromlech.browser.directives import title
from dolmen.container import IBTreeContainer
from zopache.application.interfaces import ITab
from .contents import Contents
from cromlech.security import permissions
from zopache.zmi.interfaces import IURLSegment
from zopache.zmi.interfaces import IObjectRetitler

@view_component
@name('retitle')
@title("Edit Titles")
@target(ITab)
@permissions('Manage')
@context(IBTreeContainer)
class Manage(Page,Contents):
    label=''
    subTitle='Rename Videos'
    #template = tal_template('zmi.pt')
    def getRoot(self):
           return (self.request.environ['zodb.connection'].root()
                   ['applicationRoot'])

    def renameAll(self):
        ids = self.request.POST.getall('ids_list')
        titles = self.request.POST.getall('newTitleValue:list')
        for id , title in zip (ids, titles):

            item = self.context[id]
            IObjectRetitler(item).retitleItem(item,title,self)

            
    def update(self):
        root = self.getRoot()
        self.template = root['Products']['Templates']['EditTitles']
        if 'container_rename_button' in self.request.form:
             self.renameAll()

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
@name('fix2')
@title("Fix")
@target(ITab)
@permissions('Manage')
@context(IBTreeContainer)
class Fix(Manage):
       def update(self):
          item=self.context
          import pdb; pdb.set_trace()
          fred = 1








       

       



