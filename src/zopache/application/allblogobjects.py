from zopache.pages.interfaces import IPageBase
from zope.interface import Interface
from dolmen.container import IBTreeContainer

#FROM http://codeaffectionate.blogspot.com/2013/05/tree-iterator-in-python.html
from zope.interface import Interface
class AllChildObjects:
    interface = IBTreeContainer
    
    #downTo is only used by one sub class: AllObjectsDownTo
    def __init__(self, node, interface = None, downTo = 'RSS'):
        self.stack = [node]
        self.downTo = downTo
        if interface != None:
           self.interface = interface
    
    def __iter__(self):
        return self

    def __next__(self):
        if not self.stack: raise StopIteration
        node = self.stack.pop()
        if self.interface.providedBy(node):
           for item in  node.values():
              if (self.interface.providedBy(item)):                   
                  self.stack.append(item)
        return node

class EveryObject(AllChildObjects):
    def __next__(self):
        if not self.stack: raise StopIteration
        node = self.stack.pop()
        if hasattr(node, '__dict__'):
            for item in node.__dict__.values():
               self.stack.append(item)
        if self.interface.providedBy(node):
           for item in  node.values():
              if (self.interface.providedBy(item)):                   
                  self.stack.append(item)
                  
        return node

class AllWikiObjects(AllChildObjects):
      interface = IPageBase
    
class AllBlogObjects(AllWikiObjects):
    pass

#GET ALL OF THE RSS LEAVES
class RSSLeaves(AllWikiObjects):
    def __next__(self):
        while True:
            if not self.stack:
                raise StopIteration 
            node = self.stack.pop()
            if node.__class__.__name__ == self.downTo:           
                    return node
            if self.interface.providedBy(node):
               for item in  node.values():
                    if (self.interface.providedBy(item)):                   
                       self.stack.append(item)

from zopache.remote.ivideo  import IVideo    
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

    def allChildObjects(self):
        return AllChildObjects(self)

    def everyObject(self):
        return EveryObject(self)    

    def rssLeaves(self):
        return RSSLeaves(self)            
