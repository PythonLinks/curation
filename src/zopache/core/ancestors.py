from cromlech.browser import IPublicationRoot

class Ancestors(object):
    def ancestorsExcludingSelf(self):
        return self.ancestors()[1:]
    
    def ancestors(self):
        result  = self.ancestorsUpTo(IPublicationRoot)
        return result

    def ancestorsUpTo(self, anInterface):
        ancestors=[]
        item = self
        while (item!=None):
           ancestors.append(item)
           if anInterface.providedBy(item):
              break
           item=item.__parent__      
        return ancestors
    
    @property
    def ancestorNames(self,item):
        return  [x.name for x in self.ancestors]
        
