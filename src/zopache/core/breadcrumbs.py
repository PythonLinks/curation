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
from zopache.core.uniquename import UniqueName

from zopache.ttw.acquisition import ParentalAcquire,webClassAcquire

from zopache.zmi.interfaces import IURLSegment

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
    return reversedParentsUpTo(self,IPublicationRoot)

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
import cython

class Breadcrumbs(UniqueName):
    def isCompiledByCython(self):
        return cython.compiled

    def parents(self, item=None):
        if item == None:
           item = self.context
        result  = parents(item)
        result.reverse()
        return result
    
    def safeMethod(self,attribute):
       result = getattr(self, attribute,None)
       if result:
          return result()
       result = getattr(self.context, attribute,None)
       if result:
          return result()        
       return None 

    def urlEncode(self,str):
        return urllib.parse.quote(str)
  
    def safeParentalAcquire(self,name,context=None):
          if context==None:
             context = self.context

          result = ParentalAcquire(context) [name]
          if result == None:
             return ("ERROR: " + name +
                     "DOES NOT EXIST IN THE PARENTS OF" +
                     self.href(self.url(context), context.name))
          try:
              result = result (self)
              return result
          except:
            return "ERROR IN SAFE PARENTAL ACQUIRE"

            
    def getRoot(self):
           return (self.request.environ['zodb.connection'].root()
                   ['applicationRoot'])

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
        myInterface = locate(dottedName)
        if myInterface == None:
            return False
        result = myInterface.providedBy(self.context)
        return result

    def isAuthenticated(self):
       return not IUnauthenticatedPrincipal.providedBy(self.request.principal)

    #RETURNS THE TAIL END OF THE URL 
    def slashViewName(self,item, viewName):
            if viewName == '':
                   return ''
            elif viewName=='manage':
                  viewName=IURLSegment(item).getSegment()                
            return '/' + viewName

    def IURLSegment(self,item):
        return IURLSegment(item).getSegment()                
     
    def breadcrumbsIndex(self,item):
        return self.breadcrumbsView(item,viewName='',showTitles=True)

    #THE DEFAULT BREADCRUMBS
    def breadcrumbs(self):
        return self.breadcrumbsIndex(self.context)
          
    #FOR MANAGEMENT VIEWS  
    def breadcrumbsManage(self):
        return self.breadcrumbsView(self.context,viewName='manage',showTitles=False)

    #SKIP THE CURRENT OBJECT, IF POSSIBLE
    def breadcrumbsParent(self):
        if IPublicationRoot.providedBy(self.context):
            return self.breadcrumbsIndex(self.context)
        else:
            return self.breadcrumbsIndex(self.context.__parent__)          

    #LEGACY VERSION,
    #COULD BE RETIRED
    def breadcrumbsView(self,item, viewName='',showTitles=True):
        return  self.breadcrumbsCore(item,
                                     viewName=viewName,
                                     showTitles=showTitles)
    
    #AND HERE WE HAVE THE WORKHORSE                
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
                isRoot =IPublicationRoot.providedBy(ancestor)
                if isRoot:
                   base_url=resolve_url(ancestor,self.request)
                else:
                    base_url += '/'
                    base_url+=quote(name.encode('utf-8'), _safe)
                if  not (isRoot and viewName ==''):    
                    newURL= base_url + slashViewName
                    result.append( self.href(newURL,title))
        return ' / '+' / '.join(result)

    
    def isBTreeContainer(self,*args):
        if (len (args)==0):
           return  IBTreeContainer.providedBy(self.context)    
        return  IBTreeContainer.providedBy(args[0])    

    def objectHref(self,obj,name):
        return self.href(self.url(obj),name)

    #THIS ONE IS BEING DEPRECATED
    #NOT QUITE CLEAR WHAT IT DOES
    def acquire(self,name, context=None):
        return self.parentalAcquire(name,context)
      
    def parentalAcquire (self,name,context=None):  
            if (context == None):
               context = self
            return ParentalAcquire(context)[name]
          
    def webClassAcquire(self,name,context=None):
        if context == None:
           context = self.context
        return webClassAcquire(context,name)   

    def acquireTitle(self):
        return self.acquireAttribute ( 'title')

    def acquireAttribute(self, attribute):      
        parents = lineage_chain(self.context)
        for item in parents:
            result = getattr(item,attribute,'')
            if result:
               return result
        return ''

             
    def url(self, *args):

        if len(args)==0:
            return self.request.url
        else:
            return  get_absolute_url((args)[0], self.request)

    def contextURL(self, name=''):
        itemURL = get_absolute_url(self.context, self.request)
        if name:
            itemURL += '/' + name
        return itemURL
           
    #And here is a much simpler implementation of URL.
    #Only good for this zodb application. 
    def simpleUrl(self,item):
        if IPublicationRoot.providedBy(item):
           return self.request.application_url
        container = item.__parent__
        result = self.url(container)+ '/' + item.__name__
        return result



    def shortURL(self,viewName=""):
        result = '/'
        result += self.context.__name__
        if viewName:
           result += '/' + viewName
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

    def divBreadcrumbs(self, node,viewName ='',widget= False):     
        items=list(parents(node))
        items.reverse()
        items = items [1:]
        length = len(items)
        if length > 50:
            return "ERROR IN DIV BREADCRUMBS"
        result= '<div style = "text-align:left; ">'
        target = False
        indent = -1
        for step,item in enumerate(items):
                   if widget and step > 0 and (step < length -3):
                       continue
                   if widget and (step == length -2):
                       continue                     
                   indent += 1
                   result += '<div style = "margin-left:' 
                   result +=  str(indent) + 'em">'
                   target = False
                   if widget:
                     if step == 0:
                         viewName = ''
                         target = True                        
                     if step == length -1:
                        viewName = 'showvideo'
                     if step == length -3:
                        viewName = 'videos'                        
                   slashViewName = self.slashViewName(item,viewName)
                   result += self.href(('/' + item.__name__ + slashViewName),
                                           item.title,
                                           target=target)
                   result +=  ' &nbsp;(' + str(item.branchSize) + ')'
                   result +=  '</div>'
        result += "</div>"
        return result
    
