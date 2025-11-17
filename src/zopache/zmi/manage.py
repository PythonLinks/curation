import crom
from zope.interface import implementer
from zope.interface import Interface
from zope import schema
from zope import interface

#Why does this not work?
#from cromlech.container import IOrdered
from dolmen.container import IBTreeContainer

from dolmen.forms.base import Actions
from cromlech.browser.interfaces import IPublicationRoot
from cromlech.security import Unauthorized
from dolmen.container import OrderedBTreeContainer

from .contents import Contents
from zopache.core.page  import  Page
from zopache.zmi.cutfolder import cutFolder
from . import tal_template
from zopache.core.interfaces import ITreeSecurity

from zopache.zmi.interfaces import IObjectRetitler
from zopache.pages.interfaces import IPage, IPageBase

from zopache.core.viewdecorators import *
from zopache.zmi.interfaces import IURLSegment
from zopache.zmi.actions import (
    ReName,CopyObjects, CutObjects, DeleteObjects,
    ReTitle,ReBoth,PasteObjects)
from zopache.core.baseform import Form
from zopache.python.interfaces import IDirectory
from zopache.application.root import RootContainer
from zopache.ttw.interfaces import IPrincipalFolder,IInternalPrincipal
from zopache.core.scripts import Scripts

#Breadcrumbs is included in Form
class ManageBase(Form,Contents):
    __name__ = 'manage'
    supportsPaste = True
    title = "Forest Wiki Management Interface"
    subTitle='Rename and Retitle Objects. Cut, Copy and Paste them.  '
    template = tal_template('manage.pt')
    actions= Actions()
    
    @property    
    def actions(self):
        #FIRST TEST SECURITY
        if (IPrincipalFolder.providedBy(self.context) or
            IInternalPrincipal.providedBy(self.context)):
            if not self.treeSecurity():
               raise Unauthorized()
           
        #RETURN IF THEY DO NOT HAVE PERMISSION   
        if not self.treeSecurity():        
           return Actions()

        
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
        return Actions(*actionList)


    """
    #USE THIS TO DEFINE MANAGFE TEMPLATES IN THE ZODB
          products = self.getProducts()
          self.template = self.getTemplates()['Manage.pt']
     """
    
    def isOrderedContainer(self):
        return IPageBase.providedBy(self.context)
    
    def getManageURL(self,item):
        try:
           url = self.relativeURL(item)
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


#MANAGE FILE SYSTEM DIRECTORY
#IT IS NOT A BTREE Container
@form_component
@name('manage')
@context(IDirectory)
@permissions('Manage')
class ManageDirectory (ManageBase): 
     pass
 
#THE REAL MANAGE
@form_component
@name('manage')
@context(Interface)
@implementer(ITreeSecurity)
class Manage (ManageBase):
        pass

    
#USED TO FIRE UP A DEBUGGER TO MAKE MANUAL CHANGES    
@form_component
@name('fix')
@context(IBTreeContainer)
@permissions('Manage')
class Fix(Manage):
    def make(self):
        from slugify import slugify
        from bs4 import BeautifulSoup
        from zopache.remote.rss import RSS
        data = self.context['rssFeeds'].source
        soup = BeautifulSoup(data, 'html.parser')
        publications = soup.findAll("a", {"class": "publication"})
        siteRoot = self.context.getSiteRoot()
        for rss in publications:
            new = RSS()
            url = rss["href"]
            new.remoteURL = url.split("?")[0]
            if siteRoot.existsRemoteURL(new.remoteURL):
                continue
            new.title = rss.find("div", {"class": "publication-title"}).text
            new.name = slugify(new.title)
            if new.name in siteRoot:
                continue
            
            new.rssURL = new.remoteURL  + "/feed"
            image = rss.find("img")
            new.iconURL = image["src"]
            new.description = rss.find("div",
                        {"class": "publication-description"}).text

            self.context[new.name] = new
            #siteRoot.indexItem(new)
    
    def update(self):
        ManageBase.update(self)
        item=self.context
        import pdb; pdb.set_trace()

        pass
    
    def moveTo(self,childName):
        self.moveItem('personCopy1',childName,'person')
       
    def moveItem(self, name, childName, newName):
        item = self.context [name]
        self.context[childName][newName] = item
            





       

       



