from BTrees.OOBTree import OOBTree
from zopache.pages.page import Page
from zope.interface import implementer
from zopache.business.geocoding import GeoCodeObject
from zopache.remote.video import BasicVideo
from zopache.pages.interfaces import ILocation
from zopache.core.interfaces import IVideo
from zope import schema
from zopache.pages.interfaces import IMap

class IVideoLocation(IVideo,ILocation):
    title = schema.TextLine(
        title = 'Page Name',
        description = u'What is the title for this content?',
        required = True,
    )

    description= schema.Text(
        title = u'Description (200 Characters)',
        description = "A short description of this page.",
        required = False,
        max_length = 200,
        default = '',
    )

    date = schema.Date(title='Date ',
                           description = """ Use the format Day/Month/Year""", 
                           required = True)
    
    source= schema.Text(
        title = u'More Informatton',
        description = u'Please more information about the event.',
        required = False,
        default = '',
    )

@implementer (IVideoLocation)
class VideoLocation (GeoCodeObject,BasicVideo):
    count = 0

    def __init__(self):
        BasicVideo.__init__(self)
        GeoCodeObject.__init__(self)

    def postAddProcess(self,view):
        GeoCodeObject.postAddProcess(self, view = view)
        BasicVideo.postAddProcess(self, view = view)

    def postProcess(self,view):
        GeoCodeObject.postProcess(self, view = view)
        BasicVideo.postProcess(self, view = view)        
        
