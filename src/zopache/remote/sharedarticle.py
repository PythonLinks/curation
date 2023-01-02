import time

from dolmen.container import BTreeContainer

from zopache.core.getroot import getPublicationRoot

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

   
