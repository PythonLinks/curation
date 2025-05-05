#FROM HERE WE CAN IMPORT VIDEOS
# BY CHANNEL, BY SEARCH TERM OR BY CHANNEL
from slugify import slugify
import transaction


#from apiclient.errors import HttpError
from .downloadvideolist import core
from zopache.remote.youtube.parsechannel import parseChannel
from zopache.remote.youtube.parseplaylist import parsePlayList
from zopache.core.getroot import getSiteRoot
from zopache.pages.uniquename import UniqueName
from .getvotes import getYouTubeObject

baseArgs = {}
baseArgs [ 'maxResults'] = 50
baseArgs ['publishedAfter'] = "2017-12-07T00:00:00Z"

class Base(UniqueName):
    def processResults (self,context,results,videoClass):   
        for item in results:
                  video = videoClass()
                  video.title= item['title']
                  video.videoId = item['videoId']
                  source = item ['description']
                  video.source = source
                  video.description = ''
                  name = slugify (video.title)
                  root = getSiteRoot(context)
                  name2 = root.chooseName(name,object)
                  if name != name2 :
                      print ("WARNING",video.title)
                  if not name2 in context:
                      context [name2] = video

class ByChannel(Base):                      
    def __init__(self,view,youTubeId,videoClass):
        context = view.new
        note =  "Created ByChannel:" + context.__name__ 
        transaction.get().note(note)
        args = baseArgs.copy()
        args ['channelId'] = youTubeId
        args ['part'] = 'snippet'
        search = self.search(args,context)        
        results =  core (args,search,parseChannel)
        self.processResults (context,results,videoClass)

    def getSearch (self,args,context):
         youtube = getYouTubeObject(context)        
         search_response = youtube.search().list(**args)
         search_response = search_response.execute()
         return search_response                      
    
class ByPlayList(Base):                      
    def __init__(self,view,youTubeId,videoClass):
        context = view.new
        note =  "Created PlayList:" + context.__name__ 
        transaction.get().note(note)
        args = baseArgs.copy()
        args ['playlistId']=youTubeId       
        args ['part']= 'snippet,contentDetails'
        search = self.search(args,context)
        results = core (args,search,parsePlayList)
        self.processResults (context,results)

    def getSearch (self,args,context):
        youtube = getYouTubeObject(context)
        search_response = youtube.playlistItems().list(**args)
        search_response = search_response.execute()
        return search_response

class BySearchTerm(Base):                      
    def __init__(self,view,query,videoClass):
        context = view.new
        note =  "Created Search:" + context.__name__ 
        transaction.get().note(note)
        args = baseArgs.copy()
        args ['q']=query
        args ['part']= 'snippet'
        args ['type']= 'video'
        #args ['videoDuration']= 'medium'
        args ['relevanceLanguage']= 'pl'                
        #THIS ONE WILL NOT WORK, self.search not defined. 
        search = self.search(args,context)                
        results =  core (args,search,parseChannel)        
        self.processResults (context,results,videoClass)   

        #AND NOW FOR SHORT VIDEOS
        #del args ['pageToken']
        #args ['videoDuration']= 'medium'        
        #results =  core (args,search,parseChannel)        
        #self.processResults (context,results)           
