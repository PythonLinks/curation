from slugify import slugify
from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base.markers import FAILURE
from .interfaces import IObjectCutter, IObjectCopier, IObjectRenamer
from .interfaces import IObjectPaster, IObjectDeleter
from .interfaces import IObjectRetitler, IObjectRenamer
from zopache.pages.cache import cache
from zopache.crud.utilities import title_or_name

class BaseAction(Action):
    def getValues(self,form,message,which='ids_list'):
        request = form.request
        if not hasattr(request, 'POST'):
            return []
        POST = request.POST
        ids = POST.getall(which)
        if not ids or len(ids)==0:
            form.error += message
            return []
        return ids
    
class ReName(BaseAction):
    def __call__(self,form):
        ids = self.getValues(form,
               "You did not specify any object to rename")
        newIds = self.getValues(form,
                            "You did not specify any new names",
                            which = 'newNameValue_list')
        if (len (ids) != len (newIds)):
            form.error += "Lengths of Ids and Names  do not match. "
            return
        for oldId , newId in zip (ids, newIds):
            item = form.context[oldId]
            newId = slugify (newId)
            if newId != oldId:
                renamer = IObjectRenamer(item)
                renamer.renameItem(oldId, newId,form)
        cache.resetCache()

class ReTitle(BaseAction):                
    def __call__(self,form):
        """Given a sequence of tuples of old, new ids we rename"""
        ids = self.getValues(form,
               "You did not specify any object to reTitle")
        newTitles = self.getValues(form,
                            "You did not specify any new Titles",
                            which = 'newTitleValue_list')
        if (len (ids) != len (newTitles)):
            form.error += "Lengs of Ids and Titles do not match. "
            return
        for id , newTitle in zip (ids, newTitles):        
            item = form.context[id]
            reTitler = IObjectRetitler(item)
            reTitler.retitleItem(item,newTitle,form)   


class CopyObjects(BaseAction):
    def __call__(self,form):
        """Copy objects specified in a list of object ids"""
        ids = self.getValues(form,
             "You didn't specify any ids to copy.")
        for id in ids:
            item = form.context[id]
            copier = IObjectCopier(item)
            if not copier.allowed():
                form.error += "Object "+ id + " cannot be copied"
                return
            copier.copy(form)

class CutObjects(BaseAction):
    def __call__(self,form): 
        """Cut objects specified in a list of object ids"""
        ids = self.getValues(form,"You didn't specify any ids to cut.")
        for id in ids:
            item = form.context[id]
            cutter = IObjectCutter(item)
            if not cutter.allowed():
                title = title_or_name(item)
                form.error += ("Object " +
                               id + ' ' + title + 
                               " Cannot be Cut")
                return
            cutter.cut(form)
        cache.resetCache()    

class PasteObjects(BaseAction):            
    def __call__(self,form):
        target = form.context
        paster = IObjectPaster(target)
        paster.paste(form)
        cache.resetCache()

class DeleteObjects(BaseAction):        
    def __call__(self,form):
        """Remove objects specified in a list of object ids"""
        ids = self.getValues(form,
                          "You did not select any objects to delete")
        container = form.context
        for id in ids:
            item= container [id]
            deleter = IObjectDeleter(item)
            deleter.deleteItem(form)
        cache.resetCache()



       

       


            
         # HINTS ON HOW TO DO ERRORS
         #   form.errors = errors
         #   return FAILURE
         #   form.errors.append(Error(
         #       title='Login failed',
         #       identifier=self.prefix,
         #   ))
        #raise HTTPFound(url)
