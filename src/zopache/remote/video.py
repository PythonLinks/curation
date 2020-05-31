from zopache.pages.page import Page
from zopache.core.viewdecorators import *
from zopache.remote.ivideo import IBasicVideo, IPrincipalVideo
from zopache.remote.voteable import Voteable
from zopache.remote.interfaces import IVoteable
from zopache.remote.voteable import Voteable

class VideoBase(Voteable):
    webClass='Video'
    startTime = ''
    publishedAt = 0
    seconds = 0
    minutes = 0
    hours = 0
    def isLightingTalk(self):  
        if self.__class__.__name__ == 'LightningTalk':
           return True
        if hasattr(self,'recordingType'):
            if self.recordingType =='lightning-talk':
               return True
        return False
    
    def getDefaultThumbNailURL(self):
        try:
            return self.thumbnails.get('default').get('url')
        except:
            pass
        return ""
        
    def getSrcSet(self):
        if not hasattr(self,'thumbnails'):
            return ""
        values =  self.thumbnails.values()
        result = []
        for i in values:
            try:
               aString = (i['url'] + ' ' +
                          str(i['height']) + 'h ' +
                          str(i['width']) + 'w')
               result.append(aString)
            except:
                pass
        srcset = ",".join(result)
        return srcset          

     
    def moveTo (self,view):
        request = view.request
        principal = request.principal
        if (principal.__name__ != 'lozinski'):
           return 'You are not authorized to move Videos'
        if not 'target' in request.form:
           return 'You have to define where to move the video.'
        targetName = request.form ['target']
        root = self.getSiteRoot()
        try:
           newParent = root [targetName]
        except:
            return "That is not a valid destination anme for the video"
        name = self.__name__

        # YOU HAVE ALREACY CHECKED SCRUITY
        # SO PROCESS IT
        
        del self.__parent__ [name]
        newParent [name] = self
        raise HTTPFound(location='/' +targetName  + '/manage')     
    
    def processStartTime(self, view = None):
        startTime = (self.seconds +
                             (self.minutes * 60)  +
                             (self.hours * 3600))
        self.startTime = str(startTime)                      
    
        
@implementer (IBasicVideo)     
class BasicVideo (VideoBase,Page):
    pass

@implementer (IPrincipalVideo)     
class PrincipalVideo (VideoBase,Page):
    pass

