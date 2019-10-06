import os
import subprocess

from zope import interface
from zope.interface import implementer 

from dolmen.container import IBTreeContainer
from dolmen.container import IBTreeContainer,BTreeContainer
from cromlech.webob.response import Response

from zopache.core import Leaf
from zopache.core.viewdecorators import *
from zopache.ttw.interfaces import ITestSource as ISource
from zopache.ttw.acescripts import AceScripts
from zopache.ttw.interfaces import ISourceLeaf, ISourceContainer
from zopache.ttw.interfaces import ITestURL
from zopache.ttw.javascript import JavascriptFolder

from here  import HERE
from .utils import create_directory
from zopache.python.filesystem import FileBase,DirectoryBase, Directory
from zopache.python.interfaces import IPythonFolder,IMixed
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.ttw import actions as ttwactions

from zopache.ttw.interfaces import IJavascript
from zopache.python.interfaces import IPython
from zopache.python.filesystem import DirectoryBase

#OBJECTS WHICH EXIST BOTH IN THE ZODB AND IN THE FILE SYSTEM.
class MixedBase(object):
    lastPath = ''

    #The BASE TRANSCRYPT OBJECTS GETS ITS PATH FROM ./data/files    
    def getRootPath(self):
        path = os.path.join(HERE,'data')
        path = os.path.join(path,'files')
        path = os.path.join(path,self.__name__)                
        return path
        
    def getPathFromParent(self):
        parentPath = self.__parent__.path
        name = self.__name__
        path = os.path.join(parentPath, name)
        return path            
    
    def getPath(self):
        if IMixed.providedBy(self.__parent__):    
           return self.getPathFromParent()
        else:
            return self.getRootPath()
    
    path = property (getPath)

    def setLastPath(self):
        self.lastPath = self.path

#ZODB  Object plus a file.                 
class ObjectFile(MixedBase,FileBase):

    def postAddProcess (self,view=None):
        self.setMimeType(self)        
        self.exportSource()
        self.compile(view)
        
    def postEditProcess(self,view):
        self.exportSource()
        self.compile(view)

    def preMoveProcess(self,view):
        self.setLastPath()
        
    def postMoveProcess(self,view):
        subprocess.call(['mv',self.lastPath,self.path])
        
    def preDeleteProcess(self,view):
        self.delete(view)
               
        
#ZODB plus a directory
class MixedDirectoryBase(MixedBase):
    
    def get(self,name,default=None):
        return self.__getitem__(name,default = default)

    def valuesAsList(self):
        result = []
        for item in self.values():
            result.append (item)
        return result
    
    def postAddProcess(self,view=None):
        create_directory(self.path)

    #Move is also used for rename.    
    def preMoveProcess(self,view=None):
        self.setLastPath()
        
    def postMoveProcess(self,view):
        subprocess.call(['mv',self.lastPath,self.path])

    def preDeleteProcess(self,view):
         self.delete(view)

#ZODB Leaf plus a directory        
class ObjectDirectory(Directory,MixedDirectoryBase):
    def postAddProcess (self,view=None):
        self.exportSource()
        self.compile(view)

    def postEditProcess(self,view=None):
        self.exportSource()
        self.compile(view)
        
    def __contains__(self, key):
       return key in self.fileSystemKeys()
    
    def __getitem__(self,name,default=None):        
      if name in self.fileSystemKeys():
          return self.getFileOrDirectory(name)

      # IF ALL ELSE FAILS
      return default
  
    def __delitem__(self,name,default=None):
      if name in self.fileSystemKeys():
         self[name].delete()
         return
     
      # IF ALL ELSE FAILS
      raise Exception("Failed to Delete")
  
    def values(self):
        for item in self.uniqueFileSystemKeys():
              yield self.getFileOrDirectory(item)  

    def keys(self):
        yield (self.uniqueFileSystemKeys())
        
    #There are two Python objects, one on the file system.
    #We only want the one in the zodb.      
    def uniqueFileSystemKeys(self):    
        for item in self.fileSystemKeys():
               yield(item)
        
        
#This is a Continer plus a directory
class ContainerDirectory(MixedDirectoryBase,DirectoryBase):

    def __contains__(self, key):
        return (key in self._data  or 
                key in self.fileSystemKeys())
    
    def __getitem__(self,name,default=None):
        
      if name in self._data:
         return self._data[name]
     
      if name in self.fileSystemKeys():
          return self.getFileOrDirectory(name)

      # IF ALL ELSE FAILS
      return default
  
    def __delitem__(self,name,default=None):
        
      if name in self._data:
         BTreeContainer.__delitem__(self,name)
         return
     
      if name in self.fileSystemKeys():
         self[name].delete()
         return
     
      # IF ALL ELSE FAILS
      raise Exception("Failed to Delete")
  
    def values(self):
        for item in BTreeContainer.values(self):
            yield (item)
        for item in self.uniqueFileSystemKeys():
              yield self.getFileOrDirectory(item)  

    def keys(self):
        for item in BTreeContainer.keys(self):
            yield (item)
        yield (self.uniqueFileSystemKeys())
        
    #There are two Python objects, one on the file system.
    #We only want the one in the zodb.      
    def uniqueFileSystemKeys(self):    
        for item in self.fileSystemKeys():
            if item not in self._data:
               yield(item)


@implementer(IPythonFolder)
class PythonFolder(ContainerDirectory,JavascriptFolder):
    icon="ttwicons/JavascriptFolder.svg"    

    def isPythonFolder(self):
        return True
    
    def getJavascript(self):
        return ''
    
    def getJavascriptObjects(self):
         result=[]
         for item in self.values():
             if (IJavascript.providedBy(item) or
                IPython.providedBy(item)):
                result+= item.getJavascriptObjects()
         return result

from dolmen.forms.base import Actions
from zopache.crud import actions as formactions, i18n as _
from zopache.ttw import actions as ttwactions     
@form_component
@name('addPythonFolder')
@context(IBTreeContainer)
@target(IView)
@permissions('Manage')
class AddPythonFolder(AceScripts,AceAddForm):
    subTitle= 'Add a Python Folder'
    interface = IPythonFolder
    ignoreContent = True
    factory=PythonFolder        

    @property
    def actions(self):
        return Actions(
              ttwactions.AddAndSearch(_("Add  and Search",
                                       "Add  -> Search"),
                                        self.factory),
              formactions.Cancel(_("Cancel","Cancel")))
    
