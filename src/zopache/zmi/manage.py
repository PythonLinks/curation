import crom
from zope.interface import implementer
from zope.interface import Interface
from zope import schema
from zope import interface
from dolmen.container import IBTreeContainer
from dolmen.forms.base import Actions

from .contents import Contents
from zopache.core.page  import  Page
from zopache.zmi.cutfolder import cutFolder
from . import tal_template

from zopache.zmi.interfaces import IObjectRetitler
from zopache.zmi.interfaces import IZMI

from zopache.core.viewdecorators import *
from zopache.zmi.interfaces import IURLSegment
from zopache.core.interfaces import ITreeSecurity
from zopache.zmi.actions import (
    ReName,CopyObjects, CutObjects, DeleteObjects,
    ReTitle,PasteObjects)
from zopache.core.baseform import Form
from zopache.pages.interfaces import INotPage
from zopache.python.interfaces import IDirectory

class ManageBase(Form,Contents):
    supportsPaste = True
    label=''
    subTitle='Rename Videos. Cut and Paste them.  '
    # TEMPLATE IS IN THE ZODB
    
 
    def getManageURL(self,item):
        try:
           url = self.url(item)
           segment =  IURLSegment(item).getSegment()
           return url + '/' + segment
        except:
           return "BROKEN-URL"
                
    def breadcrumbs(self):
        return self.breadcrumbsManage()

    def iconTag(self,url):
        if url [-3:]=="png":
            return """<img src="%s" width="16px" height = "16px">""" %url
        return """<div style = "width:16px; height:16px; background:
        url('%s')" ></div>""" % url 

        
    def iconHTML(self,item):
        if (hasattr(item,'icon') and
           item.icon!=''):
           return self.iconTag("/fanstatic/"+item.icon) 
        else:
           return ''
    """
    def  hasClipboardContents(self):
        if not self.supportsPaste:
            return False
        # touch at least one item to in clipboard confirm contents
        if len(cutFolder(self))> 0:
             return True
        return False
    """
    def update(self):
          root = self.getRoot()
          #self.template = root['Products']['Templates']['Manage.pt']
          self.template = root['Products']['Templates']
          try:
            self.template = self.template['EditTitles']
          except:
            self.template = self.template['Manage.pt']              
          return
      
#THE MANAGE DEMO
@form_component
@name('managedemo')
@title("Manage")
@context(IZMI)
class ManageDemo(ManageBase):
    def breadcrumbs(self):
        return self.breadcrumbsIndex(self.context)    

#MANAGE FILE SYSTEM DIRECTORY
@form_component
@name('manage')
@context(IDirectory)
@permissions('Manage')
class ManageDirectory (ManageDemo): 
    def breadcrumbs(self):
        return self.breadcrumbsManage()       
    
#THE REAL MANAGE
@form_component
@name('manage')
@title("Manage")
@context(IBTreeContainer)
@permissions('Manage')
class Manage (ManageBase):
    
    @property
    def actions(self):
        act1 = ReName("ReName","ReName")
        act2 = ReTitle("ReTitle","ReTitle")
        act3 = CutObjects  ("Cut", "Cut")
        act4 = CopyObjects ("Copy", "Copy")
        act5 = PasteObjects("Paste","Paste")
        act6 = DeleteObjects("Delete", "Delete") 
        actionList = [act1,act2,act3, act4]
        if self.hasClipboardContents():
           actionList.append (act5)
        actionList.append (act6)
        return Actions(*actionList)        
            
#USED TO FIRE UP A DEBUGGER TO MAKE MANUAL CHANGES    
@form_component
@name('fix')
@title("Fix")
@context(IBTreeContainer)
@permissions('Manage')
class Fix(Manage):

    def update(self):
        Manage.update(self)
        item=self.context
        import pdb; pdb.set_trace()
        pass





       

       



