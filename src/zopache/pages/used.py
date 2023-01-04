import time
from zopache.core.getroot import getPublicationRoot
from zopache.core.relatives import parentsWhichImplement
from zopache.pages.interfaces import ICategory,IContent

class Used(object):
    lastTootTime = 0
    _toot = ""
    
    @property
    def isVideo(self):
        return False

    def creationDateForHumans(self):
         return time.strftime("%Y-%m-%d",time.localtime(self.creationTime))

    def getToot(self, view = None):
        if self._toot != "":
            return self._toot
        else:
            return self.defaultToot(view = view)

    def setToot(self,value):
        self._toot = value

    toot = property (getToot, setToot)    
    
    def className(self):
        return self.__class__.__name__
    
    def getTitleFor(self,view):
        return self.title
    
    def getDescriptionFor(self,view):
        return self.description

    def allValuesAsList(self):
        result = []
        for item in self.values():
               result.append (item)
        return result
    
    def valuesAsList(self):
        result = []
        for item in self.values():
            if IContent.providedBy(item):            
               result.append (item)
        return result

    def getPublicationRoot(self):
        return getPublicationRoot(self)

    @property
    def titlePlusDescription(self):
        if self.description == None:
           return self.title

        return self.title + " " + self.description + " " + self.parent.title
    
    def defaultToot(self,view=None):
        return( self.title +
                "\n\n" + 
                self.description +
                "\n\n" +
                self.parentalTags() +
                "\n\n"          
        )    

    def recalculateRootJSON(self):
         jsonRoot = self.getPublicationRoot()
         if jsonRoot:
            jsonRoot.setJson()   
    
    def parentalTags(self):
        result = []
        parents = parentsWhichImplement(self,ICategory)
        for item in parents:
            tags = item.tags
            if tags != '':
               result.append(tags)
        return ' '.join(result) 

    def getTitle(self):
         return self.title

    def getTitleForDomain(self,domain):
        return self.title

    def getDescriptionForDomain(self,domain):
        return self.description

    
