from dolmen.container import IBTreeContainer
all = set()
class EveryObject:    
    interface = IBTreeContainer

    def __init__(self, node, interface = None):
        self.stack = [node]
        if interface != None:
           self.interface = interface

    def next(self):
        return self.__next__()

    def __iter__(self):
        return self
    
    def __next__(self):
        if not self.stack:
            raise StopIteration
        node = self.stack.pop()
        all.add (node)    
        if hasattr(node, '__dict__'):
            for key, value  in node.__dict__.items():
               if key in ["self", "__parent__", "len"]:
                   continue
               if value.__class__.__name__ == "Length":
                    continue
               if hasattr(value,'__dict__'):
                  self.stack.append(value)
        if self.interface.providedBy(node):
           for item in node.values():
                  self.stack.append(item)
        return  node

