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
from zopache.python.filesystem import DirectoryBase
from zopache.python.interfaces import IPythonFolder,IMixed
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.ttw import actions as ttwactions

from zopache.ttw.interfaces import IJavascript
from zopache.python.interfaces import IPython

#OBJECTS WHICH EXIST BOTH IN THE ZODB AND IN THE FILE SYSTEM.
class MixedObject(object):
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

    def deleteLastPath(self,view):        
        subrpocess.call(['rm','-r', self.lastPath])


#This is a folder which contains both ZODB and File System Objects
#It is a separate class, just to make it easier to understrand. 
class MixedFolder(MixedObject):

    def __contains__(self, key):
        return (key in self._data  or 
                key in self.fileSystemKeys())
    
    def get(self,name,default=None):
        return self.__getitem__(name,default = default)
    
    def __getitem__(self,name,default=None):
        
      if name in self._data:
         return self._data[name]
     

      if name in self.fileSystemKeys():
          return self.getFileOrDirectory(name)

      # IF ALL ELSE FAILS
      return default
  
    def valuesAsList(self):
        result = []
        for item in self.values():
            result.append (item)
        return result
    
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

    def preDeleteProcess(self,view):
        self.delete(view)
        
    def postAddProcess(self,view):
        create_directory(self.path)

    def preMoveProcess(self,view):
        self.setLastPath()
        
    def postMoveProcess(self,view):
        subprocess.call(['mv',self.lastPath,self.path])
        

@implementer(IPythonFolder)
class PythonFolder(MixedFolder,JavascriptFolder,DirectoryBase):
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
    
