import hashlib
from dolmen.container import IBTreeContainer

def hash(value):
         h = hashlib.sha256() 
         h.update(value.encode('utf-8')) # Update the hash using a bytes object
         return h.hexdigest()

def hashTime(self):
    modificationTime = getattr(self,'modificationTime',0)
    mtime = getattr(self,'_p_mtime',0)
    modificationTime = max(modificationTime, mtime)
    text = self.__name__
    if hasattr(self,'title'):
        text += self.title
    if hasattr(self,'description'):
        text += self.description
    if hasattr(self,'source'):
        text += self.source

    if not IBTreeContainer.providedBy(self):
        return hash(text), modificationTime

    for item in self.values():
        childHash, childTime = hashTime(item)
        modificationtime = max (modificationTime,childTime)
        text += childHash
    return hash(text) , modificationTime




