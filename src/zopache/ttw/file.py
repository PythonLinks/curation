

from ZODB.blob import Blob, BlobFile

from zope.interface import Interface, implementer
from dolmen.container import OrderedBTreeContainer
from zopache.core import Leaf
from zopache.ttw.interfaces import IFile

          
@implementer(IFile)
class File(Leaf):

    def __init__(self):
        self.blob = Blob()
        
    @property
    def size(self):
        return self.blob.getSize()

    def setData(self, data):
        blobFile = BlobFile(self.__name__, 'w', self.blob)
        with self.blob.open(mode ="w") as f:
           f.write(data)
        f.close()
        
    def getData(self):
        with  self.blob.open(mode='r') as f:
           return f.read()
       
    data = property(getData,setData)
    
    def postProcess(self):
        pass

    def postAddProcess(self):
        pass


class Image (File):


    def postAddProcess(self):
           self.postProcess()
    
def make_file_response(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or u'')
        response.content_type=view.context.contentType
        return response

from cromlech.webob.response import Response
from dolmen.view import View, make_view_response
from zopache.core.viewdecorators import *
@view_component
@name('index')
@context(IFile)
@title("View File")
class Index(View):
    responseFactory = Response
    make_response = make_file_response
        
    def render(self):
               return self.context.data

@view_component
@context(IFile)
@name('manage')
class ManageFile(Index):    
   pass
                
                         
