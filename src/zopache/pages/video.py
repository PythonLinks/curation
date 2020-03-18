from zopache.pages.page import Page
from zopache.core.viewdecorators import *
from .ivideo import IBasicVideo

class VideoBase(object):
    webClass='Video'
    startTime = ''
    viewCount = 0
    publishedAt = 0
    seconds = 0
    minutes = 0
    hours = 0
    
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

     
    
    def upVote(self,principal):
        self.possiblyCreateVoteCounts()
        key = principal.__name__
        if key in self._downVotes:
            del self._downVotes[key]
        if key in self._upVotes:
            del self._upVotes[key]
            return
        self._upVotes[key] = time.time()


    def downVote(self,principal):
        self.possiblyCreateVoteCounts()
        key = principal.__name__
        if key in self._upVotes:
            del self._upVotes[key]
        if key in self._downVotes:
            del self._downVotes[key]            
            return
        self._downVotes[key] = time.time()           
        
            
    def possiblyCreateVoteCounts(self):    
        if not hasattr(self,"_upVotes"):
           self._upVotes = OOBTree()
        if not hasattr(self,"_downVotes"):
           self._downVotes = OOBTree()           
        
    def processStartTime(self, view = None):
        startTime = (self.seconds +
                             (self.minutes * 60)  +
                             (self.hours * 3600))
        self.startTime = str(startTime)                      

        
@implementer (IBasicVideo)     
class BasicVideo (VideoBase):
    pass

