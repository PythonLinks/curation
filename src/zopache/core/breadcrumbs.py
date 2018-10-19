#Subject to ZPL and CV Licenses
# -*- coding: utf-8 -*-
import urllib.parse

from cromlech.browser import IPublicationRoot
from cromlech.location import lineage_chain
from cromlech.location import resolve_url
from cromlech.location import get_absolute_url
from dolmen.container import IBTreeContainer
from cromlech.browser.interfaces import IPublicationRoot
from cromlech.security.interfaces import IPrincipal ,IUnauthenticatedPrincipal


from zopache.ttw.acquisition import Acquire,ParentalAcquire

from zopache.zmi.interfaces import IURLSegment
try:
  from zopache.ttw.acquisition import Acquire
except ImportError:
  Acquire=lambda x : x      

try:
        from urllib import quote  # Python 2.X
except ImportError:
        from urllib.parse import quote  # Python 3+

_safe = '@+'  # Characters that we don't want to have quoted
def parents(item):
    return lineage_chain(item)
            
def parentWhichImplements(self,interface):
          item=self
          while (item!=None):
            if interface.providedBy(item):
                            return item
            item=item.__parent__
          return None


def reversedParents(self):
    return reversedParentsUpTo(self,IBreadcrumbsRoot)

def parentsUpTo(self,anInterface):
    return reversed(reversedParentsUpTo(self,anInterface))

def reversedParentsUpTo(self,anInterface):
        parents=[]
        item=self        
        while (item!=None):
           parents.append(item)
           if anInterface.providedBy(item):
              break
           item=item.__parent__      
        return parents



def parentWhichImplements(self,interface):
        item=self        
        while (item!=None):
           if interface.providedBy(item):
              return item
           item=item.__parent__      
        return None

def parentsWhichImplement(self,interface):
        item=self        
        result=[]
        while (item!=None):
           if interface.providedBy(item):
              result.append(item)
           item=item.__parent__      
        return result



def parentalMethod(self,method):
   for item in parents(self):
       if hasattr(item,method):
          return item.__getattr__(method)
   raise Exception("NO SUCH METHOD FOUND")

        

def nameAndTitle(item,showTitles):
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

from pydoc import locate
class Breadcrumbs(object):


    def urlEncode(self,str):
        return urllib.parse.quote(str)
  
    def parentalAcquire(self,id):
          return ParentalAcquire(self.context)[id]
  
    def getRoot(self):
           return (self.request.environ['zodb.connection'].root()
                   ['applicationRoot'])

    def hasTrueAttribute(self,attribute):
        if (hasattr(self.context, attribute) and
            getattr(self.context,attribute)):
            return True
        return False
      
    def debug(self):
        import pdb;pdb.set_trace()
        pass
      
    def debugArg(self,arg):
        import pdb;pdb.set_trace()
        pass      
      
    def implements (self,dottedName):
        myInterface = locate(dottedName)
        if myInterface == None:
            return False
        result = myInterface.providedBy(self.context)
        return result

    def isAuthenticated(self):
       return not IUnauthenticatedPrincipal.providedBy(self.request.principal)
 
    def breadcrumbsIndex(self,item):
        return self.breadcrumbsView(item,viewName='',showTitles=True)
    
    def breadcrumbsManage(self):
        return self.breadcrumbsView(self.context,viewName='manage',showTitles=False)
    
    def breadcrumbs(self):
            return self.breadcrumbsIndex(self.context)

    def breadcrumbsParent(self):
        if IPublicationRoot.providedBy(self.context):
            return self.breadcrumbsIndex(self.context)
        else:
            return self.breadcrumbsIndex(self.context.__parent__)          
            
    def breadcrumbsView(self,item, viewName='',showTitles=True):
        return  self.breadcrumbsCore(item,
                                     viewName=viewName,
                                     showTitles=showTitles)
    
    def slashViewName(self,item, viewName):      
            slashViewName =''

            if viewName == '':
                   return ''
            elif viewName=='manage':
                  viewName=IURLSegment(item).getSegment()                

            return '/' + viewName
                
    def breadcrumbsCore(self,item,
                        viewName='',
                        showTitles=True,
                        resolver=nameAndTitle):

        parents = lineage_chain(item)
        result=[]
        if parents:
            parents.reverse()

            for ancestor in parents:
                name, title = resolver(ancestor,showTitles)
                slashViewName = self.slashViewName(ancestor,viewName)
                if IPublicationRoot.providedBy(ancestor):
                   base_url=resolve_url(ancestor,self.request)
                else:
                    base_url += '/'
                    base_url+=quote(name.encode('utf-8'), _safe)
                newURL= base_url + slashViewName
                result.append( self.href(newURL,title))
        return ' / '+' / '.join(result)

    
    def isBTreeContainer(self,*args):
        if (len (args)==0):
           return  IBTreeContainer.providedBy(self.context)    
        return  IBTreeContainer.providedBy(args[0])    

    def objectHref(self,obj,name):
        return self.href(self.url(obj),name)
    
    def href(self,url,name):
           result ='<a href=\"'
           result += url
           result+='\">'
           if name != None:
              result += name
           result +='</a>'
           return result

    def acquire(self,name):
            return Acquire(self)[name]

    def acquireTitle(self):
        parents = lineage_chain(self.context)
        #parents.reverse()
        for item in parents:
            if (hasattr(item,'title') and
               item.title!=''):
               return item.title
        return ''

             
    def url(self, *args):
        if len(args)==0:
           return get_absolute_url(self.context, self.request)
        else:
            return  get_absolute_url((args)[0], self.request)
           
    #And here is a much simpler implementation of URL.
    #Only good for this zodb application. 
    def simpleUrl(self,item):
        if IPublicationRoot.providedBy(item):
           return self.request.application_url
        container = item.__parent__
        result = self.url(container)+ '/' + item.__name__
        return result



    def secureShortURL(self):
        result = 'https://'
        result += self.getDomain()
        result += '/'
        result += self.context.__name__
        return result
      
    def getDomain(self):
        return self.domain(self.context)

    def domain(self,item):
        if IPublicationRoot.providedBy(item):
           result = self.request.application_url[8:]
           result = result.lower()
           return result
        container = item.__parent__
        result = self.domain(container)
        return result      

   
    def objectHref(self,obj,name):
        return self.href(self.url(obj),name)
    
    def href(self,url,name):
           result ='<a href=\"'
           result += url
           result+='\">'
           if name != None:
              result += name
           result +='</a>'
           return result

    def divBreadcrumbs(self, node):     
        items=list(parents(node))
        items.reverse()
        result= '<br><div style = "text-align:left; ">'
        step = -1
        for item in items:
                   step += 1
                   result += '<div style = "margin-left:' 
                   result +=  str(step) + 'em">'
                   result += self.href(('/' + item.__name__),item.title)
                   result +=  ' &nbsp;(' + str(item.branchSize) + ')' 
                   result +=  '</div>'
        result += "</div>"
        return result
    
