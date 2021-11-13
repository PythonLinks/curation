from zopache.core.uniquename import UniqueName 
from slugify import slugify
from zopache.core.getroot import getPublicationRoot

class UniquePageName (UniqueName):
    def uniqueName(self,container,newName,ofType = ""):
        root = getPublicationRoot(container)
        valuesByToken = root.valuesByToken
        oldName =""
        while (newName!=oldName):
            oldName = newName
            newName = slugify(newName, lower = False)
            newName = self.uniqueContainerName(
                            container,newName,ofType);
            newName = self.uniqueContainerName(
                            valuesByToken,newName,ofType);
        return newName            
