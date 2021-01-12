import dawnlight
from cromlech.dawnlight import DawnlightPublisher
from  zopache.application.traverser import Traverser
from cromlech.dawnlight.utils import safeguard
from cromlech.browser import IPublisher, IView, IResponseFactory
from zope.interface.interfaces import ComponentLookupError
from zopache.ttw.historyitem import HistoryTraverser
from zopache.pages.interfaces import IPage,IProxyPage

from cromlech.dawnlight.publish import shortcuts, PublicationError

class Publisher (DawnlightPublisher):
    """Traverses model objects, and looks up views. 
    """
    def __init__(self,view_locator):
         self.view_locator=view_locator
         self.longPath = []
         self.shortPath = []
         self.shortPathOkay = True

    def newContext(self,newContext):
        self.longPath.append(newContext)
        
        if not IPage.providedBy (newContext):
            self.shortPathOkay = False
        if IProxyPage.providedBy (newContext):
            self.shortPathOkay = False
        if not self.shortPathOkay:
            self.shortPath.append(newContext)
            
            
    @safeguard
    def publish(self, request, root,handle_errors):
        view=None
        publisher  = self
        path = self.base_path(request)
        context=root
        hostName = request.domain
        #Maybe traverse to a lower level SiteRoot
        crumbs = dawnlight.parse_path(path, shortcuts)

        if crumbs:
             aType, name=crumbs.popleft()
             if  name in context:
                 pass
             elif  name in ['manage',
                          'fix',
                          'editors',
                          'aceedit',  
                          'addRootCategory',
                          'addPoliticiansSite',  
                          'editHosts']:
                 pass
             else:
                context = context.getSiteRootFor(hostName)
        else:
                context = context.getSiteRootFor(hostName)
                domain = hostName
                splitDomain= domain.lower().split(".")
                if len(splitDomain) == 3:
                   siteRootName = splitDomain[0]
                   if siteRootName in context:
                      context = context[siteRootName]
                
                 
        traverser=Traverser(self.view_locator)
        
        crumbs = dawnlight.parse_path(path, shortcuts)
        while crumbs:
          
           aType, name=crumbs.popleft()
           if (aType =='history'):
              # CALL THE HISTORY TRAVERSER
              historyTraverser=HistoryTraverser(context,None)
              context=historyTraverser.traverse('history',name)
              continue
          
           #NOW FOR THE REGULAR TRAVERSER
           context, view =traverser(context,request,name,publisher)
           if view != None:
                 break

        #If that did not work  check for a template or view
        if view is  None:
           name = 'index' 
           context, view=traverser(context,request,name,publisher)

        #If still no view, check for a view on the template
        if view is  None:
           name = 'index' 
           context, view=traverser(context,request,name,publisher)


        #IF A VIEW WAS FOUND, RETURN IT

        if (view is  not None):
                    view.publisher = publisher
                    factory = IResponseFactory(view)
                    response = factory()
                    return response

        raise PublicationError('%r can not be rendered.' % context)                
