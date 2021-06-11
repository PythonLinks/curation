from slugify import slugify
from slugify import slugify
from zopache.core.getroot import getSiteRoot

class UniqueName(object):
    def uniqueContainerName(self, container, new_name,ofType="-"):
        count=0
        copyName=new_name+ofType
        copyName = slugify (copyName, lower=False)
        while new_name in container:
               count +=1
               new_name=copyName+str(count)
        return new_name

    def uniqueSiteName(self, container, new_name,ofType="-"):
        siteRoot = getSiteRoot(container)
        return self.uniqueContainerName ( siteRoot, new_name,ofType)

    def uniqueBothName(self,context,name):    
        name = slugify(name,lower=True)
        newName=self.uniqueContainerName(context,name,ofType="_")        
        newName=self.uniqueSiteName(context,newName,ofType="-")
        return newName       

