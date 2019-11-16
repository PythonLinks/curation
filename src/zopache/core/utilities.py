from cromlech.security.interfaces import IPrincipal ,IUnauthenticatedPrincipal
from zopache.application.treesecurity import TreeSecurity
from dolmen.container import IBTreeContainer
from pydoc import locate

class Utilities (object):
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
        self["webPageName"] = self.context.__name__        
        if self.isAuthenticated():
            parameters["isAuthenticated"] = True
            principal = self.request.principal
            parameters["handle"]= principal.handle
            parameters["email"]= principal.email
            parameters["userId"] = principal.__name__
            parameters["permissions"]= principal.permissions
        else:
            parameters["isAuthenticated"] = False            
            parameters["handle"]= 'Anonymous'
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


