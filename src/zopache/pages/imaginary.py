from zope.interface import Interface, implementer
from dolmen.container import IBTreeContainer
from zopache.ttw.interfaces import IImage
from zopache.pages.interfaces import IImaginary, IImaginaryBTree
from zopache.pages.interfaces import IPage

    
@implementer (IImaginary)
class Imaginary(object):
    isImaginary = True
    realObject = None
    def __init__(self,parent,realObject):
        self.__parent__ = parent
        self.__name__ = parent.__name__ + '.' + realObject.__name__
        self.realObject = realObject
        
    def bestMostRecentPage(self):
        return self.realObject.bestMostRecentPage()
    
    def html(self):
        return self.realObject.html()
    def childCategories(self):
        return []
    
    def getTitle(self):
        return self.realObject.title
    def getDescription(self):
        return self.realObject.description
    def getSource(self):
        return self.realObject.source
    def getWebClass(self):
        return self.realObject.webClass
    def getWebApproved(self):
        return self.realObject.webApproved     
    
    title = property(getTitle)
    description = property(getDescription)
    source = property(getSource)
    webClass = property(getWebClass)
    webApproved = property(getWebApproved)
    

@implementer (IImaginaryBTree)
class ImaginaryBTree(Imaginary,dict):
    def __init__(self, parent,realObject):
       Imaginary.__init__(self, parent,realObject)
       dict.__init__(self)

                 
    def getImaginary(self, name,default):
        """Return the named object, or raise ``KeyError`` if the object
           is not found.
        """
        try:
           return self.__getitem__(name)
        except(KeyError):
           return default
    
    def __getitem__(self,name):

           item = self.realObject [name]
           if IImage.providedBy(item):
               return item
           if IBTreeContainer.providedBy(item):              
              return ImaginaryBTree(self,item)
           else:
              return Imaginary(self,item)

        
    def values(self):
        result = []
        realObject = self.realObject
        for item in realObject.values():
           result.append(Imaginary(self,item))
        return result
    
    def realValues(self):
        return []

    def childCategories(self):
        result =[]
        for item in self.values():
            realObject = item.realObject
            if (IPage.providedBy (realObject) and realObject.webApproved):
               result.append (item)
        return result
