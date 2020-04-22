import crom
from zope.interface import implementer
from zope.interface import Interface
from zope import schema
from zope import interface
from dolmen.container import IBTreeContainer
from dolmen.forms.base import Actions
from cromlech.browser.interfaces import IPublicationRoot

from .contents import Contents
from zopache.core.page  import  Page
from zopache.zmi.cutfolder import cutFolder
from . import tal_template

from zopache.zmi.interfaces import IObjectRetitler
from zopache.pages.interfaces import IPage

from zopache.core.viewdecorators import *
from zopache.zmi.interfaces import IURLSegment
from zopache.zmi.actions import (
    ReName,CopyObjects, CutObjects, DeleteObjects,
    ReTitle,ReBoth,PasteObjects)
from zopache.core.baseform import Form
from zopache.python.interfaces import IDirectory
from zopache.application.root import RootContainer

#Breadcrumbs is included in Form
class ManageBase(Form,Contents):
    supportsPaste = True
    label='managelabel'
    title = "Forest Wiki Management Interface"
    subTitle='Rename and Retitle Objects. Cut, Copy and Paste them.  '

    template = tal_template('manage.pt')

    actions = Actions()

    def update(self):

        if not self.treeSecurity():
            return
        act1 = ReName("ReName","ReName")
        act2 = ReTitle("ReTitle","ReTitle")
        act3 = ReBoth("ReBoth","ReBoth")        
        act4 = CutObjects  ("Cut", "Cut")
        act5 = CopyObjects ("Copy", "Copy")
        act6 = PasteObjects("Paste","Paste")
        act7 = DeleteObjects("Delete", "Delete") 
        actionList = [act1,act2]

        if IPage.providedBy(self.context):                         
            actionList.append(act3)                       
        actionList.append(act4) 
        actionList.append(act5)                     

        if self.hasClipboardContents():
           actionList.append (act6)
        actionList.append (act7)
        self.actions =  Actions(*actionList)            

    """
    #USE THIS TO DEFINE MANAGFE TEMPLATES IN THE ZODB
    def update(self):
          products = self.getProducts()
          self.template = self.getTemplates()['Manage.pt']
     """    
 
    def getManageURL(self,item):
        try:
           url = self.getZodbURL(item)
           segment =  IURLSegment(item).getSegment()
           return url + '/' + segment
        except:
           return "BROKEN-URL-AT-" + item.__name__
                
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

#THE MANAGE DEMO
@form_component
@name('managedemo')
@context(IBTreeContainer)
class ManageDemo(ManageBase):
    subTitle='Editing is disabled in the demo interface.'    
    def breadcrumbs(self):
        return self.breadcrumbsIndex(self.context)

from cromlech.security import Unauthorized
from zopache.ttw.interfaces import IPrincipalFolder
#DO NOT WANT TO SHOW CONTENTS OF
#PRINCIPAL FOLDER TO THE PUBLIC
@form_component
@name('managedemo')
@context(IPrincipalFolder)
@permissions ("Manage")
class ManageDemoPrincipalFolder(ManageBase):
    def update (self):
        if not self.isManager():
            raise Unauthorized()    
        ManageBase.update()


@form_component
@name('manage')
@context(IPrincipalFolder)
@permissions ("Manage")
class ManageDemoPrincipalFolder2(ManageBase):
    def update (self):
        if not self.isManager():
            raise Unauthorized()    
        ManageBase.update(self)        

#MANAGE FILE SYSTEM DIRECTORY
@form_component
@name('manage')
@context(IDirectory)
class ManageDirectory (ManageDemo): 
    def breadcrumbs(self):
        return self.breadcrumbsManage()       
    
#THE REAL MANAGE
@form_component
@name('manage')
@context(Interface)
class Manage (ManageBase):
    pass    


        
     
#USED TO FIRE UP A DEBUGGER TO MAKE MANUAL CHANGES    
@form_component
@name('fix')
@context(IBTreeContainer)
@permissions('Manage')
class Fix(Manage):

    def moveTo(self,childName):
        self.moveItem('personCopy1',childName,'person')
       
    def moveItem(self, name, childName, newName):
        item = self.context [name]
        self.context[childName][newName] = item
            
    def update(self):
        Manage.update(self)
        item=self.context
        import pdb; pdb.set_trace()
        pass


@form_component
@name('visitChildren')
@context(IBTreeContainer)
@permissions('Manage')
class VisitChildren(Manage):
    fix = False
    result = "Visiting Children \n"    
    def update(self):
        Manage.update(self)
        item=self.context
        self.visitChildren(item)
        
    def visitChildren(self,item):
        for child in item.values():
            if child.__parent__ == None:
               if self.fix: 
                  child.__parent__ = item
               self.result +=  child.__name__
               self.result += "<br>"

            if IBTreeContainer.providedBy(child):
               self.visitChildren(child) 
               
    def render(self):
        return self.result
    

@form_component
@name('fixParents')
@context(IBTreeContainer)
@permissions('Manage')
class FixParents(VisitChildren):
    fix = True
    result = "Fixing Parents\n"    
     

#WITHOUT THIS CANNOT MANAGE INTERNAL PRINCIPALS
# BECAUSE IT UPDATES MANAGE, RATHER THAN INTRNAL PRINCIPAL. 
from zopache.ttw.interfaces import IInternalPrincipal
@form_component
@name('manage')
@context(IInternalPrincipal)
@permissions('Manage')
class FixUsers(Manage):

    def update(self):
        Manage.update(self)




       

       



