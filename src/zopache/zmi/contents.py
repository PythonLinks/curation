#subject to the ZPL and CV Licenses

__docformat__ = 'restructuredtext'
from .cutfolder import cutFolder
import six
from six.moves import urllib_parse as urllib
from . import tal_template
from .utilities import size
import arrow
from .interfaces import IObjectCutter, IObjectCopier, IObjectRenamer
from .interfaces import IObjectPaster, IObjectDeleter
from zopache.crud.utilities import title_or_name


class Contents(object):
    error = ''
    message = ''
    normalButtons = False
    specialButtons = False
    supportsRename = False
    supportsCopy = True
    supportsDelete = True

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
    
    def listContentInfo(self):
        #returns a webob multi-dictionary
        request = self.request
        GET=           request.GET
        POST=          request.POST

        if  GET.get("container_cancel_button"):
            if POST.get("type_name"):
                del request.form['type_name']
            if POST.get("rename_ids")and POST.get("new_value"):
                del request.form['rename_ids']
            if POST.get("retitle_id") and POST.get("new_value"):
                del request.form['retitle_id']
            return self._normalListContentsInfo()

        #elif (POST.get("container_rename_button"):
            #COULD CHECK IF VALUES ARE THERE
            #and not
            #self.hasIdsCalled(POST,'rename_ids:list')):
            #self.error = "You didn't specify any ids to rename."

        elif POST.get("container_add_button"):
            if POST.get("single_type_name") \
                   and POST.get("single_new_value"):
                request.form['type_name'] = request['single_type_name']
                request.form['new_value'] = request['single_new_value']
                self.addObject()
            elif POST.get('single_type_name') \
                     and not POST.get('single_new_value'):
                request.form['type_name'] = request['single_type_name']
                request.form['new_value'] = ""
                self.addObject()

        elif POST.get("type_name") and POST.get("new_value"):
            self.addObject()
        elif POST.get("rename_ids:list") and POST.getall("new_value:list"):
            self.renameObjects()
        elif POST.get("retitle_id:list") and POST.get("new_value"):
            self.changeTitle()
        elif POST.get("container_cut_button"):
            self.cutObjects()
        elif POST.get("container_copy_button"):
            self.copyObjects()
        elif POST.get("container_paste_button"):
            self.pasteObjects()
        elif POST.get("container_delete_button"):
            self.removeObjects()
        return self._normalListContentsInfo()

    def normalListContentInfo(self):
        return self._normalListContentsInfo()

    def _normalListContentsInfo(self):
        request = self.request.POST

        self.specialButtons = (
                 'type_name' in request or
                 'rename_ids' in request or
                 ('container_rename_button' in request
                  and request.get("ids")) or
                 'retitle_id' in request
                 )
        self.normalButtons = not self.specialButtons

        info = [self._extractContentInfo(x) for x in self.context.items()]

        self.supportsCut = info
        #self.supportsCopy = info
        #self.supportsDelete = info
        self.supportsPaste = self.pasteable()
        self.supportsRename = True
        """(
             self.supportsCut and
            not IContainerNamesContainer.providedBy(self.context)
            )"""

        return info


    def _extractContentInfo(self, item):
        request = self.request.GET
        POST= self.request.POST
        rename_ids = {}
        if POST.get("container_rename_button") :
            for rename_id in POST.getall('ids:list'):
                rename_ids[rename_id] = rename_id
        elif POST.get("rename_ids" in request):
            for rename_id in POST.getall('ids:list'):
                rename_ids[rename_id] = rename_id


        retitle_id = request.get('retitle_id')

        id, obj = item
        info = {}
        info['id'] = info['cb_id'] = id
        info['object'] = obj

        info['url'] = urllib.quote(id.encode('utf-8'))
        info['rename'] = rename_ids.get(id)
        info['retitle'] = id == retitle_id


        info['icon'] = None
        dc = True#IZopeDublinCore(obj, None)
        if dc is not None:
            info['retitleable'] = True#canWrite(dc, 'title')
            info['plaintitle'] = not info['retitleable']
            if hasattr(obj,'title'):
                    title=obj.title
            else:
                title='__________'        
            info['title'] = self.objectHref(obj,title)


            info['class'] = obj.__class__.__name__ 


            info['modified']  = (
                arrow.get(obj._p_mtime).humanize()[:-3])        
            info['retitleable'] = 0
            info['plaintitle'] = 1
            info['size']=size(obj)

        return info

    def safe_getattr(self, obj, attr, default):
        """Attempts to read the attr, returning default if Unauthorized."""
        try:
            return getattr(obj, attr, default)
        except Unauthorized:
            return default

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

    def hasAdding(self):
        return True
        """Returns true if an adding view is available."""
        adding = queryMultiAdapter((self.context, self.request), name="+")
        return (adding is not None)

    def addObject(self):
        request = self.request
        if IContainerNamesContainer.providedBy(self.context):
            new = ""
        else:
            new = request["new_value"]

        adding = queryMultiAdapter((self.context, self.request), name="+")
        if adding is None:
            adding = Adding(self.context, request)
        else:
            # Set up context so that the adding can build a url
            # if the type name names a view.
            # Note that we can't so this for the "adding is None" case
            # above, because there is no "+" view.
            adding.__parent__ = self.context
            adding.__name__ = '+'

        adding.action(request['type_name'], new)

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
        import pdb; pdb.set_trace()
        
        """move objects specified in a list of object ids"""
        request = self.request
        ids = request.POST.getall('ids:list')
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
        folder = cutFolder(self)        
        if (len(folder)> 0):
                 return True
        return False

    def pasteObjects(self):
        target = self.context
        items=[]
        #BECAUSE YOU CANNOT MODIFY WHILE ITERATING OVER
        for item in cutFolder(self).values():
            items.append(item)
        for item in items:
           paster = IObjectPaster(target)
           paster.paste(self)


    def  hasClipboardContents(self):
        if not self.supportsPaste:
            return False
        # touch at least one item to in clipboard confirm contents
        if len(cutFolder(self))> 0:
             return True
        return False

    contents = tal_template('app_templates/manageFolder.pt')
    contentsMacros = contents


