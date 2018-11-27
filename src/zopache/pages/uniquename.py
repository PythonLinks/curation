from zopache.core.uniquename import UniqueName 

class UniquePageName (UniqueName):
    def uniqueName(self,container,newName,ofType = ""):
        root = container.getRoot()
        valuesByToken = root.valuesByToken
        oldName =""
        while (newName!=oldName):
            oldName = newName
            newName = self.uniqueContainerName(
                            container,newName,ofType);
            newName = self.uniqueContainerName(
                            valuesByToken,newName,ofType);
        return newName            
