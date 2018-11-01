    
import crom
from zopache.crud.interfaces import IRenameable,IDeletable,ICopyable
from zopache.core import getRoot
from zopache.pages.interfaces import IPage
from zopache.zmi.cutcopypaste import BaseClass, Cutter, Copier, Deleter
from zopache.zmi.cutcopypaste import Paster, Renamer
from zopache.pages.interfaces import IPage

from zopache.zmi.interfaces import IObjectDeleter
from zopache.zmi.utilities import pasteFolder

from zopache.core import getRoot
from zopache.zmi.interfaces import IObjectCutter
from zopache.zmi.interfaces import IObjectDeleter
from zopache.zmi.interfaces import IObjectCopier
from zopache.zmi.interfaces import IObjectRenamer
from zopache.zmi.interfaces import IObjectPaster
from zopache.core.transactionnote import TransactionNote

class LocalBase(TransactionNote):
    def printToken(self,obj, message):
        root = getRoot(obj)
        valuesByToken = root.valuesByToken
        name = obj.__name__

        if name in valuesByToken:
            print (message, "TOKEN EXITS")
        else:
            print (message , " NO TOKEN")
            
    #Delete token first, then add item
    def deleteToken(self,item):
        name = item.__name__
        root = getRoot(item)
        parent = item.__parent__
        valuesByToken = root.valuesByToken

        if not IPage.providedBy(parent):
             return

        # DO NOTHING IF THIS IS A DUPLICATE 
        if  ((name in valuesByToken) and 
            (valuesByToken[name]==item)):
            del valuesByToken[name]
            

    #Add item first, then add token     
    def addToken (self, item):
        if not IPage.providedBy(item.__parent__):
           self.view.error += name +  "NOT ADDED TO valuesByToken "
        root = getRoot(item)
        valuesByToken = root.valuesByToken
        name = item.__name__
        if name in valuesByToken:
            raise Exception()
        
        valuesByToken[name] = item

        
    def uniqueName(self,container,newName):
        root = getRoot(self.context)
        valuesByToken = root.valuesByToken
        oldName =""
        while (newName!=oldName):
            oldName = newName
            newName = Copier.uniqueName(self,container,newName);
            newName = Copier.uniqueName(self,valuesByToken,newName);
        return newName            

        
@crom.adapter
@crom.sources(IPage)
@crom.target(IObjectCopier)
class CategoryCopier(LocalBase,Copier):
    # YOU NEVER WANT TO COPY CATEGORIES
    #REALLY WANT PROXY OBJECTS
    def allowed(self):
        return False

@crom.adapter
@crom.sources(IPage)
@crom.target(IObjectCutter)
class CategoryCutter(LocalBase,Cutter):
    """Adapter for moving objects between containers
    """
    #IF IT IS A CATEOGRY DELETE FROM VALUESByTOKEN
    def cut(self,view):
        self.view = view
        obj=self.context
        if not self.allowed():
            self.view.error = obj.__name__ + " CUT IN NOT ALLOWED"
            return
        self.deleteToken(obj)
        super().cut(self) 

@crom.adapter
@crom.sources(IPage)
@crom.target(IObjectPaster)
class CategoryPaster(LocalBase,Paster):
                           
    def paste(self,view):
        self.view = view        
        """Copy this object to the `target` given.
        """
        toContainer = self.context
        fromFolder=pasteFolder(self)
        #Modifying a BTree while iterating over it does not work. 
        items=[]
        root = getRoot(self)
        items = list( fromFolder.values())                   
        for item in items:
            if not self.allowed(item):
                 self.view.error = "Not Pasted"
                 continue
            orig_name = item.__name__
            new_name=self.uniqueName(toContainer,orig_name)
            self.moveFrom(fromFolder, orig_name, toContainer, new_name)
            #self.addToken(item)  

            
              
@crom.adapter
@crom.sources(IPage)
@crom.target(IObjectRenamer)
class CategoryRenamer(LocalBase,Renamer):
    def renameItem(self, oldName, newName,view):
        self.view = view        
        if not self.allowed():
             self.view.error += oldName + " Not Allowed "
             return
        container=self.context
        obj = container.get(oldName)
        if obj is None:
            raise ItemNotFoundError(self.container, oldName)
        new_name=self.uniqueName(container,newName)
        self.deleteToken(obj)
        self.moveFrom(container,oldName, container, newName)
        #self.addToken(obj)

        
#FOR DELETING CATEGORIES
#IF VIDEO DELETE LINK FROM CONFERENCE
#IF NOT EMPTY DO NOT DELETE.
#DELTE ROOT.INDEX
@crom.adapter
@crom.sources(IPage)
@crom.target(IObjectDeleter)
class CategoryDeleter(Deleter,LocalBase):
    def deleteItem(self,view):
        self.view = view        
        contained=self.context
        name=contained.__name__
        root = getRoot(contained)
        if not self.allowed():
            self.view.error +=   name + " was not deleted. <br>"   
            self.view.error += " Maybe it still contains something"
            return
        
        #OKAY NOW DO THE WORK
        # DELETE THE CANNONICAL NAME
        # HAVE TO DO THIS FIRST
        self.describeTransaction("Deleted an object with a Canonical URL",contained)        
        self.deleteToken(contained)
        
        # DELETE THE OBJECT
        container=contained.__parent__
        del container[name]
        
        # IF IT IS A VIDEO DELETE IT FROM THE CONFERENCE
        if contained.isVideo():
           self.describeTransactionWithText("It was a Videoa Video")            
           del contained.conference.talks[name]
           
        # UNLESS IT IS THE ROOT CATEGORY, RECALCULATE THE JSON   
        # THIS SHOULD ALWAYS BE TRUE
        if IPage.providedBy (container):   
           root.recalculateRootJSON()

#THIS IS NEEDED FOR PRIVATE PARTS
#              if hasattr(item,'privatePart') and item.privatePart!=None:
#                 item.privatePart.groupPart=None
#                 item.groupDeleted=True
           
    def allowed(self):
         contained=self.context
         if  not IDeletable.providedBy(contained):
                return False
         if   (IPage.providedBy(contained)):
            for i in contained.values():
               return False
         return True    
     
