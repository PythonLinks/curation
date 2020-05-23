from zopache.core.viewdecorators import *
from zopache.business.videolocation import IVideoLocation, VideoLocation
from zopache.business.addcompany import AddBase
from zopache.pages.interfaces import IMap

@view_component
@name('addVideoLocation')
@target(IView)
@context(IMap)
class AddVideoLocation(AddBase):
    interface = IVideoLocation
    title="Add a Video at a place and time"
    factory = VideoLocation

    


    
