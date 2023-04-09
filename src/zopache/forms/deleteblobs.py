import os

from cromlech.security import permissions

from zopache.core.viewdecorators import *
from zopache.ttw.interfaces import IBranch
from zopache.core.baseform import Form
from zopache.core.breadcrumbs import Breadcrumbs

from zopache.ttw.interfaces import IFileBase

from zopache.core.interfaces import  ISiteRoot

@form_component
@context(ISiteRoot)
@target(IView)
@name("packblobs")
@permissions('Manage')
class PackBlobs(Form):
    label = 'Pack Blobs'
    title = "Delete the unused blobs"
    subTitle = "This reduces the amout of disk space needed."
    def update(self):
           status = 'The unused blobs were deleted. '
           Form.update(self)
           root = self.getZodbRoot()
           zodbPaths = []
           usedFiles = set()
           for item in root.allChildObjects():
               if IFileBase.providedBy(item):
                   zodbPaths.append(self.longPathFor(item))
                   usedFiles.add(item.blob.committed())

           root = "/app/data/Blobs"
           deletedFiles = 0
           for path, subdirs, files in os.walk(root):
              for name in files:
                  if name == ".layout":
                      continue
                  filePath = os.path.join(path, name)
                  
                  if not filePath  in usedFiles:
                       deletedFiles += 1
                       os.remove(filePath)

           status += "<br>"
           status += "Number of Used Files" + str(len(usedFiles))
           status += "<br>"                   
           status += "Deleted" + str(deletedFiles) + " files"
           status += "<br>"
           status += "Keeping the folliwng files"
           status += "<br>"                              
           for item in zodbPaths:
               status += item + "<br>"                              
           self.status = status

