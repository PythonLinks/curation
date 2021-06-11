from PIL import Image as PilImage
from PIL import Image as PilImage
from io import BytesIO
import requests
from zopache.ttw.file import BTreeImage


def createImageIn(self,response):
            content = response.content
            contentType = response.headers['content-type']
            createImageInFrom(self,content,contentType)
                                 
def createImageInFrom(self,content,contentType):
            zodbImage =BTreeImage()
            zodbImage.contentType=contentType 
            zodbImage.data = content
            pilImage = PilImage.open(BytesIO(content))
            zodbImage.width = pilImage.width
            zodbImage.height = pilImage.height
            self['Logo']= zodbImage
            zodbImage.__parent__ = self

def getImage(self,imageURL):
        try:
            response = requests.get(imageURL)
            createImageIn(self,response)
        except:
            pass

async def asyncGetImage(self,imageURL):
        try:
            response = await requests.get(imageURL)
            createImageIn(self,response)
        except:
            pass 
