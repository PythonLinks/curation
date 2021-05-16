from cromlech.security.interfaces import IPrincipal ,IUnauthenticatedPrincipal
from zopache.application.treesecurity import TreeSecurity
from dolmen.container import IBTreeContainer
from pydoc import locate
from zopache.core.interfaces import IVideo
from zopache.pages.interfaces import IImaginaryBTree

class Tests(object):
    
    def hasMembers(self):
        return hasattr(self.context,'isMember')
    
    def isPerson(self):
        return IPrincipal.implementedBy(self.context)
    
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
        return root.__class__.__name__ == 'RootPage'
        
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

    def isPython(self):
        return self.hasPermission('Manage')    
    
    def isDeveloper(self):
        return self.hasPermission('Develop')    

    def hasValue(self,attribute,*args):
        item = self.context if len(args)==0 else args [0]
        if hasattr(item, attribute):
            value = getattr(self.context,attribute,None)
            if value:
               return True
        return False

    #I DO NOT THINK THIS IS USED ANYWHERE
    #def hasTrueAttribute(self,attribute):
    #    return self.hasValue(attribute)
    
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
        item = self.context if len(args)==0 else args [0]        
        return  IBTreeContainer.providedBy(item)

    #SHOULD BE USING
    #from zopache.pages.iimaginary import IImaginaryBTree
    #BUT THAT BREAKS THE BUILD
    def isContainer(self,*args):
        item = self.context if len(args)==0 else args [0]        
        if IBTreeContainer.providedBy(item):
            return True
        if IImaginaryBTree.providedBy(item):
            return True
        return False


    
        
    
