from zopache.core.uniquename import UniqueName 

class UniquePageName (UniqueName):
    def uniqueName(self,container,newName,ofType = ""):
        root = container.getRoot()
        valuesByToken = root.valuesByToken
        oldName =""
        while (newName!=oldName):
            oldName = newName
            newName = self.uniqueContainerName(self,
                            container,newName,ofType);
            newName = self.uniqueContainerName(self,
                            valuesByToken,newName,ofType);
        return newName            
