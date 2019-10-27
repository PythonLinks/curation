import dawnlight
from cromlech.dawnlight import DawnlightPublisher
from  zopache.ttw.traverser import Traverser
from cromlech.dawnlight.utils import safeguard
from cromlech.browser import IPublisher, IView, IResponseFactory
from zope.interface.interfaces import ComponentLookupError
from zopache.ttw.historyitem import HistoryTraverser

from cromlech.dawnlight.publish import shortcuts, PublicationError
from zopache.application.virtualhost import getSiteRootFromRequest

class Publisher (DawnlightPublisher):
    """Traverses model objects, and looks up views. 
    """
    def __init__(self,view_locator):
         self.view_locator=view_locator
   
    @safeguard
    def publish(self, request, root,handle_errors):
        view=None
        path = self.base_path(request)

        #Maybe traverse to a lower level SiteRoot
        crumbs = dawnlight.parse_path(path, shortcuts)
        context=root
        if crumbs:
           aType, name=crumbs.popleft()
           if not name in context:
              if not name in ['manage','fix']: 
                 context = getSiteRootFromRequest(request,context) 
        traverser=Traverser(self.view_locator)
        
        crumbs = dawnlight.parse_path(path, shortcuts)        
        while crumbs:
           aType, name=crumbs.popleft()
           #import pdb; pdb.set_trace()
           if (aType =='history'):
              # CALL THE HISTORY TRAVERSER
              historyTraverser=HistoryTraverser(context,None)
              context=historyTraverser.traverse('history',name)
              continue
          
           #NOW FOR THE REGULAR TRAVERSER
           context, view =traverser(context,request,name)
           if view != None:
                 break

        #If that did not work  check for a template or view
        if view is  None:
           name = 'index' 
           context, view=traverser(context,request,name)

        #If still no view, check for a view on the template
        if view is  None:
           name = 'index' 
           context, view=traverser(context,request,name)


        #IF A VIEW WAS FOUND, RETURN IT 
        if (view is  not None):
                    factory = IResponseFactory(view)
                    response = factory()
                    return response

        raise PublicationError('%r can not be rendered.' % context)                
