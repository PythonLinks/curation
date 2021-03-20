09
import urllib.parse
from urllib.parse import quote
from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from cromlech.location import resolve_url
from cromlech.browser import IPublicationRoot
from zopache.zmi.interfaces import IURLSegment
from zopache.zmi.interfaces import IURLSegment
from zopache.crud.interfaces import IZodbRoot
from cromlech.browser.exceptions import HTTPTemporaryRedirect

"""
The problem is that there is a site root, and a zodb root.  They may or may 
not be the same item. 

So URL has optional parameters. 
If no parameters, get the request url. 
If an object is passed, get the url to that object. 
If a name is passed, append the name. 

In the root, maybe you need to do virtual host traversal. Not so if it is 
manage or fix.  Not so if the object exists in the root. 

I wonder if this will all work?

"""

class URLMethods(object):
    def possiblyRedirect(self):
        domain = self.acquireAttribute("domain")
        if domain == "":
            return
        currentDomain = self.getDomain()
        if domain != currentDomain:
           newURL = "https://" + domain + "/" + self.context.__name__
           raise HTTPTemporaryRedirect(newURL)
       
    #THIS IS THE GOOD ONE
    #HTTPS://Domain.Name/CanonicalName
    def secureShortURL(self,context = None):
        if context == None:
           context = self.context
        result = 'https://'
        result += self.getDomain()
        result += self.getSiteRoot().basePath
        result += self.getShortPath()
        return result
    
    def getShortPath(self):
        return self.context.__name__
        #all = []
        #for item in self.publisher.shortPath:
        #    all.append(item.__name__)
        #return "/".join(all)

    def getLongPath(self):    
        all = []
        for item in self.publisher.longPath:
            all.append(item.__name__)
        return "/".join(all)    

    
    #Another Good One
    # /CanonicalName
    def shortURL(self,viewName=""):
        result = ''
        result += self.getShortPath()
        if viewName:
           result += '/' + viewName
        return result
      
    def getDomain(self):
        return self.request.host_url.lower().split('://')[1]

    def getHost(self):
        return self.getDomain()

    def nameAndTitle(self,item,showTitles):
        """Choose a display name for the current context.
        This method has been splitted out for convenient overriding.
        """
        name = getattr(item, '__name__', None)
        title= getattr(item, 'title', None)
    
        if name is None and not IPublicationRoot.providedBy(item):
            raise KeyError('Object name (%r) could not be resolved.' % item)
    
        if (title != None) and showTitles:
            return name, title
        return name, name

    #RETURNS THE LONG PATH USING PARENTS
    def getLongURL(self,item):
        return self.absoluteURL(item)
    
    def absoluteURL(self,*args):
        item = self.context if len(args)==0 else args [0]
        isSiteRoot =IPublicationRoot.providedBy(item)
        isZodbRoot = IZodbRoot.providedBy (item)
        isRootContainer = item.__class__.__name__ == "RootContainer"
        if isRootContainer:
           return ""
        elif isSiteRoot:
           return "/" + item.__name__
        else:
           breakpoint()
           if not hasattr(item, '__parent__'):
               return 'BROKEN-NO-PARENT'
           container = item.__parent__
             
           base_url= self.absoluteURL(container)
           if not base_url or base_url[-1] != "/":
               base_url += "/"
           base_url += item.__name__
           return base_url

    def relativeURL(self,*args):        
        item = self.context if len(args)==0 else args [0]        
        isSiteRoot =IPublicationRoot.providedBy(item)
        isZodbRoot = IZodbRoot.providedBy (item)
        isRootContainer = item.__class__.__name__ == "RootContainer"

        if isRootContainer:
            base_url = ""
            return base_url
        elif isSiteRoot:
            basePath =  item.basePath
            if len (basePath) <= 1:
                return item.__name__
            if basePath [0] =="/":
                basePath = basePath [1:]
            if basePath [-0] == "/":
                basePath = basePath [0:-1]
            return basePath
        elif isZodbRoot:
            base_url = ""
            return base_url        
        else:
            container = item.__parent__
            base_url= self.relativeURL(container)+ '/' + item.__name__
            return base_url

    def absoluteSiteURL(self):
        site = self.getSiteRoot()
        return self.absoluteURL(site)    
    
    def relativeSiteURL(self):
        site = self.getSiteRoot()
        return self.relativeURL(site)

    def siteURL(self):
        return self.relativeSiteURL()    

    #And here is a much simpler implementation of URL.
    #Only good for this zodb application. 
    def simpleUrl(self,item):
        return self.absoluteURL(item)

    def urllibParseURLEncode(self,aDict):
        return urllib.parse.urlencode(aDict)
        
    def urlEncode(self,str):
        return urllib.parse.quote(str)
    
    def urlQuotePlus(self,str):
        return urllib.parse.quote_plus(str)    

    #RETURNS THE TAIL END OF THE URL 
    def slashViewName(self,item, viewName):
            if viewName == '':
                   return ''
            elif viewName=='manage':
                  viewName=IURLSegment(item).getSegment()                
            return '/' + viewName

    def IURLSegment(self,item):
        return IURLSegment(item).getSegment()
    
    #ANOTHER LONG PATH USING PARENTS
    #WORKS ON CONTEXT OR ON AN ARGUMENT
    def url(self, *args):
        try:
          if len(args)==0:
            if hasattr(self.request,'path_url'):
                return self.request.path_url
            else:
                return self.simpleUrl(self.context)
          else:
            result =  self.simpleUrl((args)[0])
            return result
        except:
            return "BROKEN-URL-IN-BREADCRUMBS"
        
    #AND YET ANOTHER LONG SIMPLE URL    
    def contextURL(self, name=''):
        itemURL = self.absoluteURL(self.context)
        if name:
            itemURL += '/' + name
        return itemURL
           
    
    def objectHref(self,obj,name):
        return self.href(self.url(obj),name)

    def canonicalHref(self,obj):
        return self.href(self.url(obj),obj.title)
    
    def viewHref(self,obj,view,name):
        return self.href(self.url(obj)+ '/' + view, name)   

    def href(self,url,name,target=False):  
           result ='<a href=\"'
           result += url
           result += '"'
           if target:
             result += ' target="_blank" '
           result+='>'
           if name != None:
                result += name
           result +='</a>'
           return result
    
