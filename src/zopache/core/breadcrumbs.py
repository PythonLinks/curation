#Subject to ZPL and CV Licenses
# -*- coding: utf-8 -*-

import json

from cromlech.browser import IPublicationRoot
from cromlech.location import get_absolute_url
from dolmen.container import IBTreeContainer
from cromlech.security.interfaces import IPrincipal ,IUnauthenticatedPrincipal
from zopache.core.uniquename import UniqueName


from zopache.core.relatives import Parents
from zopache.core.urlmethods import URLMethods
_safe = '@+'  # Characters that we don't want to have quoted

            
def parentWhichImplements(self,interface):
          item=self
          while (item!=None):
            if interface.providedBy(item):
                            return item
            item=item.__parent__
          return None


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




        



try:
   import cython
except:
   pass

from zopache.core.utilities import Utilities
from zopache.core.breadcrumbscore import BreadcrumbsCore
from zopache.core.acquisition import Acquisition
from zopache.core.urlmethods import URLMethods
from zopache.core.relatives import Parents
from zopache.core.getroot import Root

class Breadcrumbs(UniqueName,
                  Utilities,
                  BreadcrumbsCore,
                  Acquisition,
                  URLMethods,
                  Root,
                  Parents):
    try:   
      def isCompiledByCython(self):
        return cython.compiled
    except:
        pass
    
    
