import time

from BTrees.OOBTree import OOBTree

from zopache.core.viewdecorators import *
from zopache.remote.mastodon.interfaces import IMastodonAccount
from zopache.remote.mastodon.interfaces import IRemoteAccount
from zopache.application.source import Source

from zopache.crud.getimage import getImage

#all imports are used

@implementer (IMastodonAccount)
class RemoteAccount(Source):
    
    webClass = "RemoteAccount"
    htmlSummary = True
    title = ""
    twitterId = ''
    mastodonId = ''
    keepAllArticles = False
    description = ""
    def __init__(self):
         Source.__init__(self)
         self.reset()

         
    def valuesAsList(self):
        result = []
        for item in self.values():
               result.append (item)
        return result
         
    def reset(self):
         self.crawledToStart = False
         self.minId = None 
         self.maxId = None
        
    @property
    def remoteURL(self):
        blank,user, server = self.parts()
        return 'https://' + server + '/@' + user

    def parts(self):
        id = self.mastodonId
        if id[0]!='@':
            id = '@' + id
        return id.split('@')

    def userName(self):
        return "@" + self.parts()[1]
    
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

class MastodonAccount(RemoteAccount):
    pass

import crom
from zopache.zmi.interfaces import IURLSegment
@crom.adapter
@crom.sources(IRemoteAccount)
@crom.target(IURLSegment)
class IRemoteAccountAdaptor(object):
    def __init__(self,context):
        self.context=context   

    def getSegment(self):
        return 'manage'

