from ZODB.blob import Blob, BlobFile
from ZODB.POSException import POSKeyError

from zope.interface import Interface, implementer
from dolmen.container import OrderedBTreeContainer
from zopache.core import Leaf
from zopache.ttw.interfaces import IFile, IImage
from zopache.core.interfaces import ITreeSecurity
          

class FileBase(object):    

        
    @property
    def size(self):
        return self.blob.getSize()

    def setData(self, data):
        dataFile = data.file
        bits =  dataFile.read()
        if len(bits) == 0:
            return
        if not hasattr(self,'blob'):
            self.blob = Blob()
        with self.blob.open(mode ="w") as blobFile:
           blobFile.write(bits)
        self.title = data ["title"]   
        
    def getData(self):
        if not hasattr(self,'blob'):
            return ""
        try:
            with  self.blob.open(mode='r') as f:
               return f.read()
        except POSKeyError as error:
            return error.args[0]

    data = property(getData,setData)
    
@implementer(IFile)
class File(FileBase,Leaf):    
     pass
 
@implementer(IImage)
class Image (File):
    icon="ttwicons/Image.svg"
    def getHTML(self, view=None):
        url = view.url(self)
        if hasattr(self,'title'):
           title = self.title
        else:
           title = ""
        tag = F"""<img src="{url}" width ="{self.width}" height = "{self.height}" alt = "{title}">"""  
        return tag
     
def make_file_response(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.content_type=view.context.contentType
        response.write(result or u'')
        return response

from cromlech.webob.response import Response
from dolmen.view import View, make_view_response
from zopache.core.viewdecorators import *



@view_component
@name('index')
@context(IFile)
class IndexFile(View):
    responseFactory = Response
    make_response = make_file_response
        
    def render(self):
               return self.context.data

#And the same for images           
@view_component
@name('index')
@context(IImage)
class IndexImage(View):
    responseFactory = Response
    make_response = make_file_response
        
    def render(self):
               return self.context.data           


from zopache.ttw.interfaces import IInternalPrincipal           
@view_component
@name('index')
@context(IInternalPrincipal)
@title("View CV")
@implementer(ITreeSecurity)
class IndexCV(View):
    responseFactory = Response
    make_response = make_file_response
        
    def render(self):
               return self.context.data           

@view_component
@context(IFile)
@name('manage')
class ManageFile(IndexFile):    
   pass
                
                         
