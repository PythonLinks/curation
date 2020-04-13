import os
import subprocess
from zope import schema
from zope.interface import implementer

from zopache.core import Leaf
from zopache.pages.page import Page
from zopache.pages.interfaces import INotebook
from zopache.python.mixed import ObjectDirectory
from zopache.python.mixed import ObjectDirectory

import mistune
from zopache.python.filesystem import File

@implementer (INotebook)
class Notebook (Leaf,ObjectDirectory):
    #No need to create the directory,
    #Saving the file will create it. 
    title = ""
    webClass = "Notebook"
    def compile(self,view):
        path = os.path.join(self.path, self.fileName())        
        cmd = "jupyter nbconvert --template basic --to html " + path
        #subprocess.call(cmd)
        os.system (cmd)
    
    def html(self):
        name = self.fileName()[0:-6] + ".html"        
        return self[name].getSource()

    def fileName (self):
        return "notebook.ipynb"

    def exportSource(self):
        path = self.path
        if not os.path.exists(self.path):
            try:
                os.makedirs(path)                
            except OSError as exc: # Guard against race condition
                pass
              #  if exc.errno != errno.EEXIST:
              #     raise
        self.exportSourceCore()

    def exportSourceCore(self):
        path = os.path.join(self.path, self.fileName())
        with open(path,'w') as theFile:
             theFile.write(self.source)        
        
    def postAddProcess(self,view):
        fileUpload =  view.request.form['form.field._v_source']
        data = fileUpload.file.read()
        data = data.decode("utf-8")
        self.source = data
        self.exportSource()
        self.compile(view)
