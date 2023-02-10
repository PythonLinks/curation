import time

from dolmen.container import BTreeContainer

from zopache.core.getroot import getPublicationRoot
from zopache.crud.getimage import getImage


class SharedArticle(object):
    def __init__(self):
         BTreeContainer.__init__(self)
         self.creationTime=time.time()
         self.modificationTime=self.creationTime

    def __delitem__(self,key):
        siteRoot = self.getPublicationRoot()
        item = self[key]
        siteRoot.unIndexItem(item)
        BTreeContainer.__delitem__(self,key)
        
    def __setitem__(self,  key,item):
        BTreeContainer.__setitem__(self,key,item)
        siteRoot = self.getPublicationRoot()     
        siteRoot.addItem(item)         

    def preProcess(self,view):
       pass
    def postProcess(self,view):
       pass
    def postAddProcess(self,view):
       pass
    def preDeleteProcess(self,view):
       pass

    def creationDateForHumans(self):
         return time.strftime("%Y-%m-%d",time.localtime(self.importTime))

   
    def addImage(self):
           if  'Logo' in self:
               return
           imageURL = self.getImageURL()
           if imageURL:
               getImage(self,imageURL)           

    def getImageURL(self):
        if url:= getattr(self,'imageURL',None):
            return url          
        elif  hasattr(self,'links'):
            for item in self.links:
                if "image" in item.type:
                    return item.href
        return None

    
    def moveTo(self,category):
              name = self.__name__
              del self.__parent__[name]
              category [name] = self
              self.__name__ = name
  
