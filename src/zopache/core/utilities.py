import json
from cromlech.security.interfaces import IPrincipal ,IUnauthenticatedPrincipal
from zopache.application.treesecurity import TreeSecurity
from dolmen.container import IBTreeContainer
from pydoc import locate
from zopache.core.getroot import getSiteRoot
import hashlib

class Utilities (object):
    def getDefaultImage(self):
        if 'image' in self.context:
            return self.context['image']
        siteRoot = self.getSiteRoot()
        if 'Logo.png' in siteRoot:
            return siteRoot['Logo.png']
        return None

    def getSiteName(self):
        siteRoot = self.getSiteRoot()
        if hasattr(siteRoot, 'siteName'):
            return siteRoot['siteName']
        return None    
    
    def isBTreeContainer(self):
         return  IBTreeContainer.providedBy(self.context)

    def widgetJsonURL(self):
        root = self.getSiteRoot()
        categoryRoot = root.rssRoot
        uri ="https://" + self.getDomain() + "/" + categoryRoot + "/json"
        return uri
    
    def isVideo(self):
        return False

    def isConference(self):
        return False
    
    def isForestWiki(self):
        root = self.getSiteRoot()
        return root.__class__.__name__ == 'Page'
        
    def treeSecurity(self):
        tree = TreeSecurity(self)
        if (self.isAuthenticated() and
           tree.hasEditorPermission()):
            return True
        return False

    def hasPermission(self, aPermission):
        if (self.isAuthenticated() and
           aPermission in self.request.principal.permissions):
           return True
        return False

    def isManager(self):
        return self.hasPermission('Manage')
    
    def parameters(self):
        parameters = {}
        parameters["webPageName"] = self.context.__name__
        context = self.context
        title = context.title if hasattr(context,'title') else ''
        parameters["webPageTitle"] = title
        parameters ["parents"] =list(map(lambda x: x.__name__,
                                         self.parentsUpToSiteRoot()))
        parameters ["banner"] = (self.parentalAcquire("Banner.png")
                                     != None)
        parameters ["logo"] = (self.parentalAcquire("Logo.png") != None)
        parameters ["homePage"]= getSiteRoot(self.context).homePage
        
        if self.isAuthenticated():
            parameters["isAuthenticated"] = True
            principal = self.request.principal
            parameters["handle"]= principal.handle
            parameters["email"]= principal.email
            parameters["userId"] = principal.__name__
            parameters["permissions"]= list(principal.permissions)
        else:
            parameters["isAuthenticated"] = False            
            parameters["handle"]= 'Guest'
            parameters["email"]= ''
            parameters["userId"] = ''            
            parameters["permissions"]= []
        result = json.dumps(parameters)
        return result
    
    
    def safeMethod(self,attribute):
       result = getattr(self, attribute,None)
       if result:
          return result()
       result = getattr(self.context, attribute,None)
       if result:
          return result()        
       return None 


            
    def hasTrueAttribute(self,attribute):
        if (hasattr(self.context, attribute) and
            getattr(self.context,attribute)):
            return True
        return False
      
    def debug(self,*args):
        import pdb;pdb.set_trace()
        fred = 1
        if args:
          fred = args
          item = args [0]
          
    def implements (self,dottedName):
        return self.itemImplements(self.context,dottedName)
    
    def itemImplements(self, item, dottedName):
        myInterface = locate(dottedName)
        if myInterface == None:
            return False
        result = myInterface.providedBy(item)
        return result

    def isAuthenticated(self):
       return not IUnauthenticatedPrincipal.providedBy(self.request.principal)

    def isBTreeContainer(self,*args):
        if (len (args)==0):
           return  IBTreeContainer.providedBy(self.context)    
        return  IBTreeContainer.providedBy(args[0])    

    def hash(self,value):
         h = hashlib.sha256() 
         h.update(value.encode('utf-8')) # Update the hash using a bytes object
         return h.hexdigest()

    def longestName(self,context,*args):
        if (len (args)==0):
           pass 
