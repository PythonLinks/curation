import crom
from zope import schema
from zope import interface
from cromlech.container.interfaces import IBTreeContainer
from zopache.zmi.new.contents import Contents
from zopache.core.page  import  Page

from . import tal_template
from crom import target, order
from dolmen.view import name, context, view_component
from cromlech.browser.directives import title
from dolmen.container import IBTreeContainer
from zopache.application.interfaces import ITab
from zopache.zmi.interfaces import IURLSegment
from zopache.zmi.interfaces import IObjectRetitler
from zopache.categories.baseedit import BaseEdit

@view_component
@name('manage')
@title("Manage")
@target(ITab)
@context(IBTreeContainer)
class Manage(BaseEdit,Page,Contents):
    label=''
    subTitle='Rename Videos. Cut and Paste them.  '
    # TEMPLATE IS IN THE ZODB
    
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
        elif 'container_cut_button' in self.request.form:
             self.cutObjects()             

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
@context(IBTreeContainer)
class Fix(Manage):
       def update(self):
          item=self.context
          import pdb; pdb.set_trace()
          fred = 1








       

       



