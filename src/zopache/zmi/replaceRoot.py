from zopache.categories.category import RootCategory
from zopache.application.root import RootContainer
def replace (context,childName,aClass):
        child = context [childName]
        new = aClass()
        new.title = child.title
        new.description = child.description
        new.source = child.source
        items = child.allValuesAsList()
        breakpoint()
        for item in items:                
            itemName = item.name
            print (itemName)
            if itemName == 'person':
               del new ['person']
            del child[itemName]
            new [itemName] = item
        fred = 2
        import pdb; pdb.set_trace()
        breakpoint()
        del context [childName]             
        context [childName] = new

def newRoot(self):
         import pdb; pdb.set_trace()
         connRoot = self.request.environment['zodb.connection'].root()
         name = "applicationRoot"
         parent = connRoot 
         replace (parent, name, RootContainer)
         context = parent [name]
         # AND NOW REPLACE THE PYTHON CATEGORY WITH A ROOT CATEGORY
         replace(context, 'python', RootCategory)
         people = context['person']
         del context ['person']
         python = context ['python']
         #del python ['person']
         python ['person'] = people
