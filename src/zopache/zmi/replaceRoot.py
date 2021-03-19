
from zopache.application.root import RootContainer

def replace (context,childName,aClass):
        child = context [childName]
        new = aClass()
        new.title = child.title
        new.description = child.description
        new.source = child.source
        items = child.allValuesAsList()
        for item in items:                
            itemName = item.name
            if itemName == 'person':
               del new ['person']
            del child[itemName]
            new [itemName] = item
        del context [childName]             
        context [childName] = new
        new.__name__ = childName
"""
from zopache.categories.interfaces import IRootCategory

def updatePrincipalFolders(self):
    for item in self.context.values():
        if IRootCategory.providedBy(item):
           item['person'].convert()     


from zopache.categories.category import RootCategory        
def newRoot(self):
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
"""
