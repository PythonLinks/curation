#Subject to the Zope and CV Licesnse

# SO HERE WE HAVE A CUSTOM TRAVERSER.
# IT TRAVERSES TO THE OBJECT AND LOOKS UP THE VIEW
# IT ALSO HANDLES CASES WHERE THE TEMPLATE IS LOOKED UP IN THE PARENTS
# SO IT IS A LITTLE BIT TRICKY, BUT MINIMAL ADAPTATION
# MAKES IT EASIER TO UNSERSTAND
from zope.interface.interfaces import ComponentLookupError
from copy import copy 
from dolmen.container import IBTreeContainer
from .interfaces import IAceHTML
from .acquisition import getFromWebClass
from zopache.core import getRoot

class Traverser(object):
    def __init__(self,view_lookup):
        self.view_lookup=view_lookup
        self.zopacheTemplate = None

    def __call__(self,context,request,name):
        #A HACK TO FIX AN IURL PROBLEM
        if name == 'root':
            return context, None
        #FIRST, IF YOU HAVE A TEMPLATE, SEE THE VIEW
        if self.zopacheTemplate != None :
           zopacheTemplate = self.zopacheTemplate
           try: 
              view = self.view_lookup(request, zopacheTemplate, name)
           except ComponentLookupError:


              #This allows us to pass arguments in the URL after
              # the template name
              view = self.view_lookup(request, zopacheTemplate, 'index')
           
           if view == None :
              raise NotFound(zopacheTemplate, name, request)              

           if hasattr(view, 'setDisplayObject'):
                view.setDisplayObject(zopacheTemplate)           
                view.context=context  
                return context, view
           else:
                 raise Exception (
                     "%s does not support method setZopacheTempalte",
                                   zopacheTemplate.__name__)
        #TRAVERSE THE CONTAINER
        if IBTreeContainer.providedBy(context):
            item = context.get(name,object)
            if item != object:
                return item, None
               
        #Now check the webclass for the object

        if hasattr(context, "webClass") and context.webClass != None:

               webClass =  context.webClass
               if isinstance(webClass, str):
                    root =getRoot(context)
                    products = root["Products"]
                    webClass = products[webClass]
               item = getFromWebClass (webClass,name,object)
               if item != object:
                  if IAceHTML.providedBy(item):
                     self.zopacheTemplate = item
                     return context,None
                  else:
                     return item, None
                 

        #CHECK FOR A VIEW ON THE CONTEXT
        view = self.view_lookup(request, context, name)
        if view is not None:
              return context, view
               

        raise NotFound(self.context, name, request)
 


        
