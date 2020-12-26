from PIL import Image as PilImage
from PIL import Image as PilImage
from io import BytesIO
import requests
from zopache.ttw.file import BTreeImage

def getImage(self,imageURL):
        try:
            response = requests.get(imageURL)            
            zodbImage =BTreeImage()
            zodbImage.contentType=response.headers['content-type']            
            content = response.content
            zodbImage.data = content
            pilImage = PilImage.open(BytesIO(content))
            zodbImage.width = pilImage.width
            zodbImage.height = pilImage.height
            self['Logo']= zodbImage
            zodbImage.__parent__ = self
        except:
            pass 
