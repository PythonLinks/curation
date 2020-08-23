from zopache.pages.interfaces import IPage
from dolmen.container import IBTreeContainer
from zopache.pages.iimaginary import IImaginary
from zopache.pages.imaginary import Imaginary, ImaginaryBTree


class ImaginaryPage(object):
    def getRealObject(self):
        siteRoot = self.getSiteRoot()    
        realObject = siteRoot[siteRoot.templateRoot]
        return realObject
    
    realObject = property(getRealObject)
    
    def childCategories(self):
        result =[]
        for item in self.values():
            if (IPage.providedBy (item) and item.webApproved):
               result.append (item)
        result += self.imaginaryCategories()
        return result
    
    def imaginaryCategories(self):
        result = []
        if not hasattr(self,'remoteURL') or self.remoteURL == "":
            for proxy in self.imaginaryValues():
                item  = proxy.realObject
                if (IPage.providedBy (item) and item.webApproved):
                   result.append (proxy)
               
        return result
    
    """    
    def allValues(self):
       real = list(self.values())
       imaginary = self.imaginaryValues()
       return real
    """
    def imaginaryValues(self):
        result = []
        realObject = self.realObject
        for item in realObject.values():
            if IBTreeContainer.providedBy(item):
              new = ImaginaryBTree(self,item)
            else:
              new = Imaginary(self,item)
            result.append(new)  
        return result
    
    def getImaginary(self,shortName,default = None):
        siteRoot = self.getSiteRoot()
        realObject = siteRoot[siteRoot.templateRoot]
        if shortName in realObject:
           item = realObject [shortName]
           if IBTreeContainer.providedBy(item):              
              return ImaginaryBTree(self,item)
           else:
              return Imaginary(self,item)
        return default

