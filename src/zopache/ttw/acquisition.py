from zope.location.location import LocationIterator
from zope.interface import Interface
from dolmen.container import IBTreeContainer

def getFromWebClass(aClass, name, marker):
    #COUNTER TO CATCH INEVITABLE INFINITE LOOP
    counter=1

    while (True):
       if IBTreeContainer.providedBy (aClass):
            result =aClass.get(name, marker)

            #IF THE WebCLASS CONTAINS THE OBJECT
            if result != marker:
               return result

       if not hasattr(aClass,'webClass'):
           return marker

       if aClass.webClass == None:
           return marker
         
       counter += 1    
       if counter > 100:
           raise Exception("YOU ARE IN AN INFINITE LOOP OF WEBClasses")

       #AND NOW REPEAT THE LOOP WITH THE PARENT WEBCLASS
       aClass=aClass.webClass


# JUST  PARENTAL (NO ZCLASS) ACQUISITION OF OBJECTS IN CONTAINERS
class ParentalAcquire (object):
  def __init__(self,context):
      self.context=context
      
  def __getitem__(self,name,default=object) :
     context=self.context
     _marker = default  

     #FIRST SEE IF THIS ITEM HAS THE VALUE
     if hasattr(context, '__getitem__'):
            result =context.get(name, _marker)
            if result!=_marker:
               return result

     #IF NOT CHECK THE PARENT CLASSES
     for item in LocationIterator(self.context):
       if hasattr(item, '__getitem__'):
         result =item.get(name, _marker)
         if result!=_marker:
            return result

class Acquire(ParentalAcquire):
    pass






