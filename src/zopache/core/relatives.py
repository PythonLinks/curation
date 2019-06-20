

class Parents(object):
    def __init__(self,context):
        self.context = context
        
    def parentsWhichImplement(self,interface):
           item=self.context
           result=[]
           while (item!=None):
             if interface.providedBy(item):
                       result.append(item)
             item=item.__parent__
           return result    
