import urllib.parse
from urllib.parse import quote
from urllib.parse import quote_plus
from cromlech.location import resolve_url
from cromlech.browser import IPublicationRoot
from zopache.zmi.interfaces import IURLSegment
from zopache.zmi.interfaces import IURLSegment
from zopache.crud.interfaces import IZodbRoot


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


    #AND HERE WE HAVE THE WORKHORSE                
    def breadcrumbsCore(self,
                        item,
                        viewName='',
                        showTitles=True,
                        ):

        parents = self.lineage(item)
        result=[]
        if parents:
            parents.reverse()
            for ancestor in parents:
                name, title = self.nameAndTitle(ancestor,showTitles)
                slashViewName = self.slashViewName(ancestor,viewName)
                base_url = self.getLongURL(ancestor)
                newURL= base_url + slashViewName
                result.append( self.href(newURL,title))
        return ' / '+' / '.join(result)

    def getLongURL(self,item):
        return self.getZodbURL(item)
    def getZodbURL(self,item):
        isZodbRoot = IZodbRoot.providedBy (item)
        if isZodbRoot:
            base_url = ''
        else:
           container = item.__parent__
           base_url= self.getLongURL(container)+ '/' + item.__name__
        return base_url        
    
    
    def getSiteURL (self,item):
        isSiteRoot =IPublicationRoot.providedBy(item)
        isZodbRoot = IZodbRoot.providedBy (item)
        if isZodbRoot:
            base_url = ''
        elif isSiteRoot:
            base_url = '/' + item.__name__
        else:
           container = item.__parent__
           base_url= self.getLongURL(container)+ '/' + item.__name__
        return base_url        

    #And here is a much simpler implementation of URL.
    #Only good for this zodb application. 
    def simpleUrl(self,item):
        return self.getSiteURL(item)        
    
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

    def url(self, *args):
        try:
          if len(args)==0:
            return self.request.url
          else:
            result =  self.simpleUrl((args)[0])
            return result
        except:
            return "BROKEN-URL-IN-BREADCRUMBS"
        
    def contextURL(self, name=''):
        itemURL = self.simpleURL(self.context)
        if name:
            itemURL += '/' + name
        return itemURL
           

    def secureShortURL(self):
        result = 'https://'
        result += self.getDomain()
        result += '/'
        result += self.context.__name__
        return result

    def shortURL(self,viewName=""):
        result = '/'
        result += self.context.__name__
        if viewName:
           result += '/' + viewName
        return result
      
    def getDomain(self):
        return self.request.host_url.lower().split('://')[1]

    def getHost(self):
        return self.getDomain()

    """
    #Maybe he next one should be retired, 
    def domain(self,item):
        if IPublicationRoot.providedBy(item):
           result = self.request.application_url[8:]
           result = result.lower()
           return result
        container = item.__parent__
        result = self.domain(container)
        return result      
    """
    
    def objectHref(self,obj,name):
        return self.href(self.url(obj),name)
 
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

#viewName=viewName,
#showTitles=showTitles)
    
    
