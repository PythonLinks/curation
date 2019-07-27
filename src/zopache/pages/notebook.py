import os
from zope.interface import implementer

from zopache.pages.page import Page
from zopache.pages.interfaces import INotebook
from zopache.python.filesystem import Directory
from zopache.python.folder import MixedObject

import mistune

@implementer (INotebook)
class Notebook (Directory,MixedObject,Page):
    #No need to create the directory,
    #Saving the file will create it. 
    def __init__(self):
        Page.__init__(self)
        
    def compile(self):
        cmd = ""
        os.system(cmd)

    def html(self):
        return self._html

    #THIS IS USED BY Python / TRANSCRYPT OBJECTS
    def deleteJavascriptObject(self,view):
        pass





