from time import time
from cromlech.security import Unauthorized
from zopache.pages.addpage import AddAuthorizedPage
from zopache.core.interfaces import ITreeSecurity,IUserSecurity
from zopache.core.viewdecorators import *
from zopache.ttw.interfaces import IInternalPrincipal
from zopache.remote.youtube.getvotes import getVideoDetails
from zopache.remote.ivideo import IBasicVideo , IPrincipalVideo
from zopache.remote.video import BasicVideo, PrincipalVideo
from zopache.pages.interfaces import IPageBase
from zopache.pages.page import Page

class Base(AddAuthorizedPage):
     interface = IPrincipalVideo
     title = "Add a  Video"
     webClass='Video'
     count = 0
     def factory(self):
          new = self.factoryClass()
          root = self.getSiteRoot()
          importTime = int(time())
          new.setImportTime(importTime,root)
          return new
     
#ADD VIDEO ELSEWHERE
@view_component
@name('addVideo')
@target(IView)
@context(IPageBase)
@implementer(ITreeSecurity)
class AddBasicVideo(Base):
     subTitle ="To this page."
     interface = IBasicVideo 
     factoryClass = BasicVideo
          
     def postAddProcess(self,view = None):
         Page.postAddProcess(self.new,view = self)
         self.context.webApproved = True
         self.context.publicationApproved = True         
         self.new.processStartTime()         

         
#ADD VIDEO TO A PRINCIPAL
@view_component
@name('addPrincipalVideo')
@target(IView)
@context(IInternalPrincipal)
@implementer(IUserSecurity)
class AddPrincipalVideo(Base):
     factoryClass = PrincipalVideo     
     subTitle ="Until it is approved, you can edit this video."
     layoutName = "UserMenu"     
     preamble = """
    <p>Use this form to add a video to this website.  
    Usually a YouTube Video is just a single video.  Sometimes there are  
    multiple lightning talks in a single video.  Here each lightning talk is 
    its own data structure, with a searchable description, and its own a 
    vote count.</p>  

    <p>What I recommend is to record a 5 minute lightning talk, 
    followed by a longer   technical video.  That way the users can decide whether they want to watch
    the whole thing or not.<p> 
     """

     def update(self):
         Base.update(self)
         if self.context != self.request.principal:
            raise Unauthorized()
     
     def postAddProcess(self,view = None):
         Page.postAddProcess(self.new,view = self) 
         parent = self.new.__parent__
         self.new.speaker = parent.name
         self.new.webApproved = False
         if not hasattr(parent, 'videos'):
             parent.videos = PersistentList()
         parent.videos.append(self.new.name)
         getVideoDetails(self.new)
         self.new.processStartTime()       

         
