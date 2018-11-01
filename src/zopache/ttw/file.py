from zopache.core.viewdecorators import *
from cromlech.file import  IFile
from zope.interface import implementer
from ZODB.blob import Blob, BlobFile

@implementer(IFile)
class File(BlobFile):

   def __init__(self, filename=None, ct=None, data=None):
     self.filename = filename
     self.content_type = ct
     self.blob = Blob(data)

   @property
   def size(self):
      return self.blob.getSize()

   def setData(self, data):
      import pdb; pdb.set_trace()
      with blob.open('w') as f:
           f.write(data)

   def getData():
      with blob.open('r') as f:
           return f.read(data)


   data = property(getData,setData)

   
@form_component
@name('addFile')
@context(IBTreeContainer)
#@target(ITab)
@title("Add File")
@permissions('Manage')
class AddCSS(AddForm):
    subTitle='Add a File'
    interface = IFile
    ignoreContent = True
    factory=File
