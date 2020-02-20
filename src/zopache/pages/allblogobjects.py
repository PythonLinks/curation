from zopache.pages.interfaces import IPage

#FROM http://codeaffectionate.blogspot.com/2013/05/tree-iterator-in-python.html
class AllBlogObjects:
 
    def __init__(self, node, interface = None):
        if interface == None:
           interface = IPage
        self.interface = interface   
        self.stack = [node]
 
    def __iter__(self):
        return self

    def next(self):
        return self.next()
    
    def __next__(self):
        interface = self.interface
        if not self.stack: raise StopIteration
        node = self.stack.pop()
        for item in  node.values():
             if (interface.providedBy(item)):                   
                  self.stack.append(item)
        return node

