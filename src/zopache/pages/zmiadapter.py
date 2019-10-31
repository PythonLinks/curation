    
import crom
from zopache.crud.interfaces import IRenameable,IDeletable,ICopyable
from zopache.core.getroot import getSiteRoot
from zopache.pages.interfaces import IPage
from zopache.zmi.cutcopypaste import BaseClass, Cutter, Copier, Deleter
from zopache.zmi.cutcopypaste import Paster, Renamer
from zopache.pages.interfaces import IPage
from zopache.pages.uniquename import UniquePageName

from zopache.zmi.interfaces import IObjectDeleter
from zopache.zmi.cutfolder import cutFolder


from zopache.zmi.interfaces import IObjectCutter
from zopache.zmi.interfaces import IObjectDeleter
from zopache.zmi.interfaces import IObjectCopier
from zopache.zmi.interfaces import IObjectRenamer
from zopache.zmi.interfaces import IObjectPaster
from zopache.core.transactionnote import TransactionNote
from zopache.core.getroot import getSiteRoot
from zopache.pages.cache import cache

class LocalBase(BaseClass):
    def printToken(self,obj, message):
        root = getSiteRoot(obj)
        valuesByToken = root.valuesByToken
        name = obj.__name__

        if name in valuesByToken:
            print (message, "TOKEN EXITS")
        else:
            print (message , " NO TOKEN")
            
    #Delete token first, then add item
    def deleteToken(self,item):
        name = item.__name__
        root = getSiteRoot(item)
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
           self.view.error += item.__name__ +  "NOT ADDED TO valuesByToken "
        root = getSiteRoot(item)
        valuesByToken = root.valuesByToken
        name = item.__name__
        if name in valuesByToken:
            raise Exception()
        
        valuesByToken[name] = item

                
@crom.adapter
@crom.sources(IPage)
@crom.target(IObjectCopier)
class CategoryCopier(LocalBase,Copier):
    # YOU NEVER WANT TO COPY CATEGORIES
    #REALLY WANT PROXY OBJECTS
    def allowed(self,item):
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
        if not self.allowed(obj):
            self.view.error = obj.__name__ + " CUT IN NOT ALLOWED"
            return
        self.deleteToken(obj)
        super().cut(view)
        cache.resetCache(view.context)
        
@crom.adapter
@crom.sources(IPage)
@crom.target(IObjectPaster)
class CategoryPaster(LocalBase,Paster,UniquePageName):
                           
    def paste(self,view):
        self.view = view        
        """Copy this object to the `target` given.
        """
        toContainer = self.context
        fromFolder=cutFolder(view)
        #Modifying a BTree while iterating over it does not work. 
        items=[]
        items = list( fromFolder.values())                   
        for item in items:
            if not self.allowed(item):
                 self.view.error = "Not Pasted"
                 continue
            orig_name = item.__name__
            new_name=self.uniqueName(toContainer,orig_name,"Copy")
            self.moveFrom(fromFolder, orig_name, toContainer, new_name)
            #self.addToken(item)  
        cache.resetCache(view.context)

            
class ItemNotFoundError(Exception):
    pass
@crom.adapter
@crom.sources(IPage)
@crom.target(IObjectRenamer)
class CategoryRenamer(LocalBase,Renamer,UniquePageName):
    def renameItem(self, oldName, newName,view):
        self.view = view
        item = self.context[oldName]
        if not self.allowed(item):
             self.view.error += oldName + " Not Allowed "
             return
        container=self.context
        obj = container.get(oldName)
        if obj is None:
            raise ItemNotFoundError(self.container, oldName)
        newName=self.uniqueName(container,newName)
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
        if not self.allowed(contained):
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
        #Have to do this before deleting the __parent__ Pointer. 
        if IPage.providedBy (container):
            root = getSiteRoot(contained)
        del container[name]
        
        # IF IT IS A VIDEO DELETE IT FROM THE CONFERENCE
        if contained.isVideo():
           self.describeTransactionWithText("It was a Videoa Video")            
           del contained.conference.talks[name]
           
        # UNLESS IT IS THE ROOT CATEGORY, RECALCULATE THE JSON   
        # THIS SHOULD ALWAYS BE TRUE
        if IPage.providedBy (container):
           root.recalculateRootJSON()
        cache.resetCache(view.context)

#THIS IS NEEDED FOR PRIVATE PARTS
#              if hasattr(item,'privatePart') and item.privatePart!=None:
#                 item.privatePart.groupPart=None
#                 item.groupDeleted=True
           
    def allowed(self,item):
         if  not IDeletable.providedBy(item):
                return False
         if   (IPage.providedBy(item)):
            for i in item.values():
               return False
         return True    

from zopache.zmi.interfaces import IURLSegment
from zopache.pages.interfaces import INotebook     
@crom.adapter
@crom.sources(INotebook)
@crom.target(IURLSegment)
class IPNotebookAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'source'        
