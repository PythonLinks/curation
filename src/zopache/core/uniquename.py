
class UniqueName(object):
    def uniqueContainerName(self, container, new_name,ofType="#"):
        count=0
        copyName=new_name+ofType
        while container.has_key(new_name):
               count +=1
               new_name=copyName+str(count)
        return new_name

    def uniqueName(self, container, new_name,ofType="#"):
        return self.uniqueContainerName ( container, new_name,ofType)

