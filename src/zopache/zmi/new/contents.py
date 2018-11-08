#subject to the ZPL and CV Licenses

__docformat__ = 'restructuredtext'
from zopache.zmi.utilities import getRoot
from zopache.zmi.utilities import pasteFolder
from . import tal_template
from zopache.zmi.utilities import size
import arrow
from zopache.zmi.interfaces import IObjectCutter, IObjectCopier, IObjectRenamer
from zopache.zmi.interfaces import IObjectPaster, IObjectDeleter
from zopache.crud.utilities import title_or_name
from zopache.zmi.cutcopypaste import Cutter, Paster, Copier, Deleter
from .adapter import ZMIAdapter as Adapter

class Contents(object):
    error = ''
    message = ''
    supportsCut = True
    supportsCopy = True
    supportsDelete = True
    supportsRename = True

    def contents(self):
        result = []
        for item in self.context.values():
            result.append (Adapter(item,self))
        return result
    
    #Check if any ids in a WebOb request.POST
    def hasIds(self,POST):
        return self.hasIdsCalled(POST,"ids:list") 

    def hasIdsCalled(self,POST,name):
            result=POST.getall(name)
            if result==None:
               return False
            if len(result)==0:
                return False
            return True
    

    def renameObjects(self):
        """Given a sequence of tuples of old, new ids we rename"""
        request = self.request
        ids = request.POST.getall("rename_ids:list")
        newids = request.POST.getall("new_value:list")
        for oldid, newid in zip(ids, newids):
            if newid != oldid:
                renamer = IObjectRenamer(self.context[oldid])
                renamer.renameItem(oldid, newid,self)

    def changeTitle(self):
        """Given a sequence of tuples of old, new ids we rename"""
        request = self.request
        id = request.get("retitle_id")
        new = request.get("new_value")

        item = self.context[id]
        dc = IDCDescriptiveProperties(item)
        dc.title = new
        notify(ObjectModifiedEvent(item, Attributes(IZopeDublinCore, 'title')))


    def removeObjects(self):
        """Remove objects specified in a list of object ids"""
        request = self.request
        POST = request.POST
        ids = POST.getall('ids:list')
        if not ids or len(ids)==0:
            self.error = "You didn't specify any ids to remove."
            return

        container = self.context
        for id in ids:
            contained = container [id]
            deleter = IObjectDeleter(contained)
            deleter.deleteItem(self)

    def copyObjects(self):
        """Copy objects specified in a list of object ids"""
        request = self.request

        POST = request.POST
        ids = POST.getall('ids:list')
        if not ids or len(ids)==0:
            self.error = ("You didn't specify any ids to copy.")
            return

        for id in ids:
            ob = self.context[id]
            copier = IObjectCopier(ob)
            if not copier.allowed():
                m = {"name": id}
                title = title_or_name(ob)
                if title:
                    m["title"] = title
                    self.error = "Object cannot be copied"
                else:
                    self.error = "Object cannot be copied"
                return
            copier.copy(self)


    def cutObjects(self): 
        """move objects specified in a list of object ids"""
        request = self.request
        ids = request.POST.getall('ids_list')
        if not ids or (len(ids)==0):
            self.error = ("You didn't specify any ids to cut.")
            return
        for id in ids:
            ob = self.context[id]
            cutter = self.cutter=IObjectCutter(ob)
            if not cutter.allowed():
                m = {"name": id}
                title = title_or_name(ob)
                if title:
                    m["title"] = title
                    self.error =  "Object '${name}' (${title}) cannot be moved"
                else:
                    self.error = "Object '${name}' cannot be moved"

                                  
                return
            cutter.cut(self)

    def pasteable(self):
        """Decide if there is anything to paste
        """
        folder = pasteFolder(self)        
        if (len(folder)> 0):
                 return True
        return False

    def pasteObjects(self):
        target = self.context
        items=[]
        #BECAUSE YOU CANNOT MODIFY WHILE ITERATING OVER
        for item in pasteFolder(self).values():
            items.append(item)
        for item in items:
           paster = IObjectPaster(target)
           paster.paste(self)


    def  hasClipboardContents(self):
        if not self.supportsPaste:
            return False
        # touch at least one item to in clipboard confirm contents
        if len(pasteFolder(self))> 0:
             return True
        return False



