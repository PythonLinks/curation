import json
from pydoc import locate
import hashlib
from cromlech.security import Unauthorized
from dolmen.message.utils import send
from zopache.core.getroot import getSiteRoot

class Utilities (object):
    def shouldDisplay(self):
        if self.context.private == False:
           return
        if self.context.private == True:
           if self.treeSecurity():
              return
        self.raiseUnauthorized()
        
    def shortenURL(self,url):        
        return url
    
    def rename(self,item,newName):
        parent = item.__parent__
        del parent[item.__name__]
        parent[newName] = item
        item.__parent__ = parent
        item.__name__ = newName

    def className(self):
        return self.__class__.__name__
    def contextClassName(self):
        return self.context.__class__.__name__    
    
    def message(self,message):
        send(message)

    def raiseUnauthorized(self):
        raise Unauthorized
    
    def getNavBar(self):
         return self.webClassAcquire('navbar.py')(self)
  
    def getDefaultImage(self):
        image  = self.parentalAcquire('SocialMediaImage')
        if image == None:
            image = self.parentalAcquire('Logo')
        return image

    def getSiteName(self):
        siteRoot = self.getSiteRoot()
        if hasattr(siteRoot, 'siteName'):
            return siteRoot['siteName']
        return None    
    
    def widgetJsonURL(self):
        siteRoot = self.getSiteRoot()
        categoryName = siteRoot.categoryName
        uri = "/" + categoryName + "/json"
        return uri
    
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
        parameters ["logo"] = (self.parentalAcquire("Logo") != None)
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


    def debug(self,*args):
        import pdb;pdb.set_trace()
        fred = 1
        if args:
          fred = args
          item = args [0]
          

    def hash(self,value):
         h = hashlib.sha256() 
         h.update(value.encode('utf-8')) # Update the hash using a bytes object
         return h.hexdigest()

    def longestName(self,context,*args):
        if (len (args)==0):
           pass 
