from cromlech.security.interfaces import IPrincipal ,IUnauthenticatedPrincipal
from zopache.application.treesecurity import TreeSecurity
from dolmen.container import IBTreeContainer
from pydoc import locate
from zopache.core.interfaces import IVideo

class Tests(object):
    
    def hasMembers(self):
        return hasattr(self.context,'isMember')
    
    def isVideo(self,*item):
        if item:
           item = item[0]
        else:
           item = self.context 
        return IVideo.providedBy (item)

    def isConference(self):
        return False
    
    def isForestWiki(self):
        root = self.getSiteRoot()
        return root.__class__.__name__ == 'Page'
        
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

    def hasValue(self,attribute):
        return self.hasTrueAttribute(attribute)
    
    def hasTrueAttribute(self,attribute):
        if (hasattr(self.context, attribute) and
            getattr(self.context,attribute)):
            return True
        return False

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
    
