from zope.interface import Interface, implementer

class IImaginary(Interface)
   pass

    
@implementer IImaginary
class Imaginary(object):

    realObject = None
    def __init__(self,parent,realObject):
        self.__parent__ = parent
        self.__name__ = parent.__name__ + '.' + realObject.__name__

    def getTitle(self):
        return realObject.title
    def getDescription(self):
        return realObject.description
    def getSource(self):
        return realObject.source
    def getWebCLass(self):
        return realObject.webClass
    def getWebApproved(self):
        return realObject.webApproved     
    
    title = property(getTitle)
    description = property(getDescription)
    source = property(getSource)
    webClass = property(getWebClass)
    webApproved = property(getWebApproved)
    

@implementer ImaginaryBTree    
class ImaginaryBTree(Imaginary):
    def values(self):
        retult = []
        for item in realObject.values():
           result.append(Imaginary(self,item))
           
    def realValues(self):
        return []
