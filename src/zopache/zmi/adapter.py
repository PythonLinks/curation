# THIS CLASS ADAPTS THE CONTEXTS
# TO DISPALY THE STUFF THE MENU NEEDS

import arrow
import crom
import transaction
from slugify import slugify
from zope.interface import Interface
from zopache.crud.interfaces import IRenameable,IDeletable,ICopyable
from zopache.zmi.interfaces import IObjectRetitler
from zopache.zmi.cutcopypaste import BaseClass
from dolmen.container import IBTreeContainer
from zopache.pages.interfaces import IPageBase
from zopache.ttw.interfaces import IAceHTML

#GENERIC RETITLER
#IF STATEMENT FOR CONFERENCE VIDEOS
@crom.adapter
@crom.sources(Interface)
@crom.target(IObjectRetitler)
class ReTitler(BaseClass):
    def __init__(self, object):
        self.context = object.__parent__
        self.__parent__ = object.__parent__ # TODO: see if we can automate this

         
    def retitleItem(self, item ,newTitle, view):

        if not self.allowed():
            self.view.error += item.__name__ + " WAS NOT ReTitled <br>"
            return
        
        self.view = view
        container=item.__parent__

        item.title = newTitle

        if hasattr(item,'isVideo') and item.isVideo():           
            oldName = item.__name__
            newName = slugify (newTitle)
            newName=view.uniqueName(container,newName)
            self.moveFrom(container,oldName, container, newName)
            conference = item.conference
            del conference.talks[oldName]
            conference.talks [newName] = item
            
    def allowed(self):
        return True
        #if  IRetitleable.providedBy(self.context):
        #        return True
        #return False


class ZMIAdapter(object):
      plainTitle = True
      reTitleable = True
      reNameable = True
      def __init__(self,obj,view):
          self.context = obj
          self.view = view
          self.request = view.request

      def editTag(self):
          context = self.context
          edits = {
              "InternalPrincipal":"permissions",
              "PrincipalFolder":"index"
          }
          className =  context.__class__.__name__
          if className in edits:
              return "/" + edits [className]
          if IPageBase.providedBy(context):
              return "/edit"
          if IAceHTML.providedBy(self.context):
              return "/aceedit"
          if "Folder" in className:
              return "/search"
          return "/aceedit"
      
      def isBTreeContainer(self):
          item = self.context 
          return  IBTreeContainer.providedBy(item)

      def getId(self,name):
          return self.context.__name__ + '-' + name

      def checkBoxId(self):
          return  self.getId('checkBox')

      def editTitleId(self):
          return  self.getId('editTitle')          

      
      def showTitleId(self):
          return  self.getId('showTitle')          

      
      def editNameId(self):
          return  self.getId('editName')          


      def showNameId(self):
          return  self.getId('showName')          

      def titleName(self):
          return self.context.__name__+ '-Title'

      def nameName(self):
          return self.context.__name__+ '-Name'

      def title(self):    
            if hasattr(self.context,'title'):
                    return self.context.title
            else:
                return self.context.__name__        

      def id(self):
           return self.context.__name__

      def name(self):
           return self.context.__name__       
       
      def object(self):
           return self.context
     
      def url (self):
          return self.view.url(self.context)
    
      def manageLink(self):
           return self.objectHref(self.url()+'/manage2',self.context.title)
       
      def contextClassName(self):
            return self.context.__class__.__name__

      def size (self):
            if IBTreeContainer.providedBy(self.context):
                return len(self.context)
            return ""

      def modified (self):
          if self.context._p_mtime != None:
              return arrow.get(self.context._p_mtime).humanize()[:-3]
          else:
              return ""

