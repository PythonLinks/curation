from PIL import Image as PilImage
from PIL import Image as PilImage
from io import BytesIO
import requests
from zopache.ttw.file import BTreeImage


def createImageIn(self,response,name = 'Logo'):
            content = response.content
            contentType = response.headers['content-type']
            createImageInFrom(self,content,contentType,name)
                                 
def createImageInFrom(self,content,contentType,name):
            zodbImage =BTreeImage()
            zodbImage.contentType=contentType 
            zodbImage.data = content
            try:
               pilImage = PilImage.open(BytesIO(content))
            except:
               print  ("FAILED TO CREATE IMAGE IN " + self.name)         
               return         
            zodbImage.width = pilImage.width
            zodbImage.height = pilImage.height
            self[name]= zodbImage
            zodbImage.__parent__ = self

def getImage(self,imageURL, name = 'Logo'):
        if not imageURL:
           return         
        try:
            response = requests.get(imageURL)
            createImageIn(self,response, name)
        except:
            pass

