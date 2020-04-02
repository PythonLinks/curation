from cromlech.security import Unauthorized
from zopache.pages.addpage import AddPageBase
from zopache.core.interfaces import ITreeSecurity,IUserSecurity
from zopache.core.viewdecorators import *
from zopache.ttw.interfaces import IInternalPrincipal
from zopache.categories.data.youtube.getvotes import getVideoDetails
from zopache.categories.data.youtube.getvotes import getVideoDetails
from zopache.remote.ivideo import IBasicVideo , IPrincipalVideo
from zopache.remote.video import BasicVideo, PrincipalVideo
from zopache.pages.interfaces import IPage
from zopache.pages.page import Page

class Base(AddPageBase):
     interface = IPrincipalVideo
     title = "Add a  Video"
     webClass='Video'
     count = 0



#ADD VIDEO TO A PRINCIPAL
@view_component
@name('addVideo')
@target(IView)
@context(IInternalPrincipal)
@implementer(IUserSecurity)
class AddPrincipalVideo(Base):
     factory = PrincipalVideo     
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
         getVideoDetails(self.new)
         
#ADD VIDEO ELSEWHERE
@view_component
@name('addBasicVideo')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddBasicVideo(Base):
     factory = BasicVideo
     subTitle ="To this page."
     interface = IBasicVideo
     def postAddProcess(self,view = None):
         Page.postAddProcess(self.new,view = self)
         getVideoDetails(self.new)     
         self.context.webApproved = True
         self.new.processStartTime()         
