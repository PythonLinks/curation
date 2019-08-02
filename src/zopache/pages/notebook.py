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
        pass
    

    def html(self):
        name = self.fileName()[0:-6] + ".html"        
        return self[name].getSource()

    def fileName (self):
        return "notebook.ipynb"
    
    def exportSource(self):
        path = os.path.join(self.path,self.fileName())
        super(Notebook,self).exportSource(path = path)

    def postAddProcess(self,view):
        fileUpload =  view.request.form['form.field._v_source']
        data = fileUpload.file.read()
        data = data.decode("utf-8")
        self.source = data
        self.exportSource()
        self.compile(view)
