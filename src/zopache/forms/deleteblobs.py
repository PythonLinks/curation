import os

from cromlech.security import permissions

from zopache.core.viewdecorators import *
from zopache.ttw.interfaces import IBranch
from zopache.core.baseform import Form
from zopache.core.breadcrumbs import Breadcrumbs

from zopache.ttw.interfaces import IFileBase


@form_component
@context(IBranch)
@target(IView)
@title("Pack")
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
           usedFiles = set()
           usedNames = []
           allFiles = set()
           for item in root.allChildObjects():
               if IFileBase.providedBy(item):
                   usedNames.append(self.longPathFor(item))
                   usedFiles.add(item.blob.committed())

           root = "/app/data/Blobs"
           for path, subdirs, files in os.walk(root):
              for name in files:
                  allFiles.add (os.path.join(path, name))

           status += "<br>"
           status += "Number of Files" + str( len(allFiles))
           status += "<br>"
           
           for item in allFiles.copy():
               if item in usedFiles:
                   allFiles.remove (item)
           status += "Number of Used Files" + str(len(usedFiles))
           status += "<br>"                   
           status += "Removing " + str(len(allFiles)) + " files"
           status += "<br>"
           status += "Keeping the folliwng files"
           status += "<br>"                              
           for item in usedNames:
               status += item + "<br>"                              
           self.status = status
           for item in allFiles:
                os.remove(item)

