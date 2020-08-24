#subject to the ZPL and CV Licenses

__docformat__ = 'restructuredtext'
from zopache.zmi.cutfolder import cutFolder
from . import tal_template
from zopache.zmi.utilities import size
import arrow
from zopache.zmi.interfaces import IObjectCutter, IObjectCopier, IObjectRenamer
from zopache.zmi.interfaces import IObjectPaster, IObjectDeleter
from zopache.crud.utilities import title_or_name
from zopache.zmi.cutcopypaste import Cutter, Paster, Copier, Deleter
from .adapter import ZMIAdapter as Adapter
from zopache.pages.iimaginary import IImaginary

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
            if not IImaginary.providedBy(item):
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
    

    def pasteable(self):
        """Decide if there is anything to paste
        """
        folder = cutFolder(self)        
        if (len(folder)> 0):
                 return True
        return False
           

    def  hasClipboardContents(self):
        if not self.supportsPaste:
            return False
        # touch at least one item to in clipboard confirm contents
        if len(cutFolder(self))> 0:
             return True
        return False



