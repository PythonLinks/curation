import time

from BTrees.OOBTree import OOBTree

from zopache.core.viewdecorators import *
from zopache.remote.mastodon.interfaces import IMastodonAccount
from zopache.application.source import Source

from zopache.crud.getimage import getImage

#all imports are used

@implementer (IMastodonAccount)
class MastodonAccount(Source):
    webClass = "RemoteAccount"
    htmlSummary = True
    title = ""
    twitterId = ''
    mastodonId = ''
    keepAllArticles = False

    def __init__(self):
         self.reset()
         Source.__init__(self)
         
    def reset(self):
         self.crawledToStart = False
         self.minId = None 
         self.maxId = None
        
    @property
    def remoteURL(self):
        blank,user, server = self.parts()
        return 'https://' + server + '/@' + user

    def parts(self):
        return self.mastodonId.split('@')
    
    def postAddProcess(self,view = None):
        if self.logoURL:
            getImage(self,self.logoURL)

    #COPY OF THIS HERE AND IN RSS.PY    
    def fetchArticles(self,feeds,view):    
        result = fetchAll(feeds,view)
        for item in result:
            if item[0] ==  FAILURE:  
               view.submissionErrors.append( "ERROR:" + str(item [1:]))
        self.status='RSS Feeds were downloaded.'
        
import crom
from zopache.zmi.interfaces import IURLSegment
@crom.adapter
@crom.sources(IMastodonAccount)
@crom.target(IURLSegment)
class IMastodonAccountAdaptor(object):
    def __init__(self,context):
        self.context=context   

    def getSegment(self):
        return 'manage'

