from cromlech.location import lineage_chain
from cromlech.browser import IPublicationRoot
from cromlech.location import lineage_chain
from zopache.crud.interfaces import IZodbRoot


def parentsUpTo(self,anInterface):
    return reversed(reversedParentsUpTo(self,anInterface))

class Parents(object):
    def __init__(self,context):
        self.context = context

    def parentalMethod(self,context,method):
       for item in self.lineage(context):
           if hasattr(item,method):
              return item.__getattr__(method)
       raise Exception("NO SUCH METHOD FOUND")


    def reversedParentsUpTo(self,item,anInterface):
        parents=[]
        while (item!=None):
           parents.append(item)
           if anInterface.providedBy(item):
              break
           item=item.__parent__      
        return parents



    def parentsUpToSiteRoot(self):
        parents = self.reversedParentsUpToSiteRoot(self.context)
        parents.reverse()
        return parents
    
    def reversedParentsUpToSiteRoot(self,item):
        return self.reversedParentsUpTo(item,IPublicationRoot)

    def reversedParentsUpToZodbRoot(self,item):
        return self.reversedParentsUpTo(item,IZodbRoot)    
        
    def parentsWhichImplement(self,interface):
           item=self.context
           result=[]
           while (item!=None):
             if interface.providedBy(item):
                       result.append(item)
             item=item.__parent__
           return result    

    def parents(self, item=None):
        if item == None:
           item = self.context
        result  = parents(item)
        result.reverse()
        return result
       
    def lineage (self,item):
        return lineage_chain(item)

    def siblings (self,item):
        breakpoint()
        if item.__parent__ == None:
            return []
        if not hasattr(item.__parent__,'childCategories'):
            return []
        siblings = item.__parent__.childCategories()
        siblings.remove (item)        
        return siblings

