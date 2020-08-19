from zopache.pages.interfaces import IPage
from zope.interface import Interface
from dolmen.container import IBTreeContainer

#FROM http://codeaffectionate.blogspot.com/2013/05/tree-iterator-in-python.html
from zope.interface import Interface
class AllChildObjects:

    def __init__(self, node, interface = Interface):
        self.stack = [node]
        self.interface = interface
        
    def __iter__(self):
        return self

    def next(self):
        return self.next()
    
    def __next__(self):
        if not self.stack: raise StopIteration
        node = self.stack.pop()
        if IBTreeContainer.providedBy(node):
           for item in  node.values():
              if (self.interface.providedBy(item)):                   
                  self.stack.append(item)
        return node


class AllBlogObjects(AllChildObjects):
      pass

#DELETES ALL BUT CATEGORY OBJECTS
#    def __next__(self):
#        if not self.stack: raise StopIteration
#        node = self.stack.pop()
#        for item in  node.allValuesAsList():
#              if (item.__class__.__name__ == 'Category'):
#                  self.stack.append(item)
#              else: 
#                  del item.__parent__[item.__name__]
#        return node    


from zopache.pages.interfaces import IPage
class AllWikiObjects(AllChildObjects):
    def __init__(self, node):
        return self.AllChildObjects(node,interface = IPage)

from zopache.core.interfaces  import IVideo    
class AllVideoObjects(AllChildObjects):
    def __next__(self):
        while True:
           nextItem = AllChildObjects.__next__(self)
           if IVideo.providedBy (nextItem):
              yield nextItem      


class ProcessTree(object):
    def allChildrenOfClass(self,className):
        result = []
        for item in AllChildObjects(self):
            if item.__class__.__name__ == className:
               result.append(item)
        return result
    
    def allBlogObjects(self):
        return AllBlogObjects(self)

    def allWikiObjects(self):
        return AllWikiObjects(self)        

    def allVideoObjects(self):
        return AllVideoObjects(self)
              
