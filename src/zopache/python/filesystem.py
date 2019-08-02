# -*- coding: utf-8 -*-

import os
import subprocess
import stat
import shutil
from mimetypes import guess_type
from persistent import Persistent
from zope.interface import implementer 

from .utils import create_directory
from zopache.core.viewdecorators import *
from here  import HERE
from zopache.python.interfaces import IPython, IPythonIndex,IPythonFile
from zopache.python.interfaces import IDirectory, IJavascriptFile
from zopache.ttw.interfaces import IJavascript, IJavascriptIndex

CHUNK_SIZE = 1 << 12

class FileAndDirectoryBase(object):
    def displayResult(self,result,view):                             
        view.error += result.stderr or ""
        view.error += result.stdout or ""
    
    def getMTime(self):
           return os.path.getmtime(self.path)
    
    _p_mtime = property (getMTime)    

    def exportSource(self, path = None):

        if not path:
           path = self.path
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                   raise
        self.exportSourceCore(path)
        
    def exportSourceCore(self,path):    
        with open(path,'w') as theFile:
             theFile.write(self.source)
    
    
class FileIterator(object):
    chunk_size = CHUNK_SIZE

    def __init__(self, f):
        self.fp = f

    def __iter__(self):
        return self

    def next(self):
        chunk = self.fp.read(self.chunk_size)
        if not chunk:
            self.fp.close()
            raise StopIteration
        return chunk

        
class FileBase(FileAndDirectoryBase):
    title = ""
    iterator = FileIterator
    size = 0
    
    def setMimeType(self, mime=None):
             self.mime = mime or guess_type(self.__name__)    

    def delete(self,view):        
        subprocess.call(['rm', self.path])            
        #self.displayresult(result,view)

    def __iter__(self):
        return iter(self.iterator(open(self.path, 'rb')))


@implementer (IJavascriptFile)
class File (FileBase):
    def __init__(self, path, name, mime=None):
             self.path = path
             self.__name__ = name
             self.mime = mime or guess_type(self.__name__)

    def getSource(self):
        with open(self.path,'r') as theFile:
             return theFile.read()
         
    source = property(getSource)
    #Used by the zmi to look like a zodb object.     

    def getJavascript(self):
        return self.source

    def delete (self,view):
        os.remove(self.path)

@implementer(IPythonFile)    
class PythonFile(File):
    pass

@implementer(IJavascriptFile)
class JavascriptFile(File):
   pass


class DirectoryBase(FileAndDirectoryBase):
    def getTitle(self):
        return self.path
    
    title = property (getTitle)
    def getSize(self):
        try:
            result = os.path.getsize(self.path)
        except:
            result = 'N/A'
        return result    

    size = property(getSize)
    
    def containsFileOrDirectory(self, name):        
        name = os.path.basename(name)
        path = os.path.join(self.path, name)
        return os.path.exists(path)
    
    def get(self,name,default):
        return self.getFileOrDirectory(name,default = default)
    
    def getFileOrDirectory(self,name,default = None):
        name = os.path.basename(name)
        path = os.path.join(self.path, name)
        if os.path.exists(path):
            if os.path.isfile(path):
               if name[-3:] == ".py" :
                    new =  PythonFile(path,name)
                    
               elif name[-3:] == ".js":
                    new =  JavascriptFile(path,name)
               else:
                    new =  File(path,name)         

            #NOT A FILE, MUST BE A FOLDER
            else:
                   new = Directory(path,mkdir = False)           
                   new.__name__ = name
               
            new.__parent__ = self
            return new
        
        return default

    def fileSystemKeys(self):
        path  = self.path
        if not os.path.isdir(path):
            return []
        return sorted(os.listdir(self.path))

    def delete(self,view):
        subprocess.call(['rm','-r', self.path])
        #self.displayresult(result,view)
        
    def rename(self, src, dst):
        dst = os.path.basename(dst)
        if dst not in self:
            if src in self:
                target = os.path.join(self.path, dst)
                source = os.path.join(self.path, src)
                shutil.move(source, target)
                return dst, target
            else:
                raise KeyError("%r doesn't exists in %r" % (dst, self.path))
        else:
            raise KeyError('%r already exists in %r' % (dst, self.path))

@implementer (IDirectory)        
class Directory(DirectoryBase):
    def contains__(self, name):
        return self.containsFileOrDirectory(name)
    
    def __getitem__(self, name, default = None):
        return self.getFileOrDirectory(name, default)

    def __iter__(self):
        for k in self.keys():
            yield self.__getitem__(k)

    def values(self):
        for k in self.fileSystemKeys():
            yield self.__getitem__(k)

    def keys(self):
        return self.fileSystemKeys()



        
