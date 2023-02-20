from bs4 import BeautifulSoup

from zopache.pages.page import Page
from zopache.core.viewdecorators import *
from zopache.remote.ivideo import (IBasicVideo,
                                   IPrincipalVideo,
                                   IEmbedVideo,
                                   IJSVideo)
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
    tags = ''
    _toot = ''
    importTime = 0
    lastTootTime = 0
    publicationApproved = True
    
    def lastTooted(self, view = None):
        if self.lastTootTime == 0:
           lastTooted = "My first toot of this video. "
        elif view == None:
           lastTooted = "ERROR CANNOT DISPLAY LAST TOOT TIME "           
        else:
            lastTooted = "Last Tooted " + view.ago(self.lastTootTime)
        return lastTooted

    def timeFreeToot(self):
         content = self._toot
         content = content.splitlines()
         
         for i, line in enumerate(content):
               if "Last tooted" in line:
                     content[i] = "" 
         
         separator = '\n'
         content = separator.join(content)        
         self._toot = content
         return content
     
    def getToot(self, view = None):
        if self._toot:
           return self._toot
        else:
            return self.defaultToot(view = view)
              
    def defaultToot(self,view = None):
        result =  self.title +"\n\n" 
        result += self.description + "\n\n"
        result += "Read more in /" + self.parent.name
        result += "\n\n"        
        if view:
           if not view.isManager():
               result += "Via @UncensoredNews@Msatodon.Social \n\n"
           result +=  "https:// " + view.secureShortURL(self.parent)[8:]
           result +=  "\n\n" 
        result += self.getRemoteURL()
        result += "\n\n"
        result +=  (
                self.parentalTags() +
               " #video #videos "
                   )
        return result
    
    def isVideo(self):
        return True
    
    def setImportTime(self,importTime,root):
        importTime = int(importTime)
        while (True):
           if not root.hasAnythingAt(importTime):
                break;
                importTime += 1
        self.importTime = importTime
    
    def isLightingTalk(self):  
        if self.__class__.__name__ == 'LightningTalk':
           return True
        if hasattr(self,'recordingType'):
            if self.recordingType =='lightning-talk':
               return True
        return False

    #For Legacy compatibility. 
    def getVideoURL(self):
        return  "https://youtube.com/embed/" + self.videoId

    
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
    videoId = ""
    def getWideFrame(self):
        return self.getIFrame(True)
    
    def getFlexFrame(self):
        return self.getIFrame(False)               
        
    def getIFrame(self,wide):
      if self.videoId == "":
             return "No Video Id"
      iFrameId = f"{self.name + '-video'}"   
      result = f"""  
        <iframe width="560" 
                id = "{iFrameId}"
                #onload = "{'resizeOneWide' if wide else 'resizeOneFlex'}('{self.name}')"
                class = "YouTubeVideo"
                height="315"
     src="https://www.youtube.com/embed/{self.videoId}?start={self.startTime}
                frameborder="0" 
                allow = "encrypted-media" 
                allowfullscreen=""></iframe>"""
      return result

@implementer (IEmbedVideo)     
class EmbedVideo (VideoBase,Page):
    def getWideFrame(self):
        return self.getIFrame(True)
    
    def getFlexFrame(self):
        return self.getIFrame(False)               

    def getRemoteURL(self):
        soup = BeautifulSoup(self.embed, 'html.parser')

        url = soup.find("iframe")["src"]
        return url
    
    def getIFrame(self,wide):
        iFrameId = f"{self.name + '-video'}"           
        embed = self.embed
        if "<iframe " in self.embed:
          splitOn = "<iframe "
        elif "<video " in self.embed:            
          splitOn = "<video "
        else:
            return "PROBLEM WITH THE EMBED TAG NOT iframe nor video"
        split = embed.split(splitOn)
        if len (split) > 1:
           result =  splitOn
           result += ' class = "YouTubeVideo" '
           result += f' id = "{iFrameId}" '
           #result +=  f""" 
           #onload = "{'resizeOneWide' if wide else 'resizeOneFlex'}('{self.name}') """
           result += split[1]
           return result
        return "Problem with the embed tag for this video. "


#NOT YET USED, FOR EMBEDDING JAVASCRIPT.    
@implementer(IJSVideo)    
class JSVideo(VideoBase,Page):
    videoId = ""
    def getWideFrame(self):
        return self.getIFrame(True)
    
    def getFlexFrame(self):
        return self.getIFrame(False)               
        
    def getIFrame(self,wide):
        return self.embed
        
@implementer (IPrincipalVideo)     
class PrincipalVideo (VideoBase):
    pass

