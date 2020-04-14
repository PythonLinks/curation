from slugify import slugify
import transaction

from apiclient.discovery import build
from apiclient.errors import HttpError
from .getvideos import core
from .parsePlayList import parsePlayList, parseChannel

#There are two copies of this key
DEVELOPER_KEY = "AIzaSyAOHmZ91f6qIt6FTi5BdopElujsENSKeN0"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

from zopache.categories.category import ConferenceVideo
from zopache.core.getroot import getSiteRoot


from zopache.pages.uniquename import UniqueName
class Base(UniqueName):
    def processResults (self,context,results):   
        for item in results:
                  video = ConferenceVideo()
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

baseArgs = {}
baseArgs [ 'maxResults'] = 50
baseArgs ['publishedAfter'] = "2017-12-07T00:00:00Z"

def search(args):
     search_response = youtube.search().list(**args)
     search_response = search_response.execute()
     return search_response
                      
class ByChannel(Base):                      
    def __init__(self,view,youTubeId):
        context = view.new
        note =  "Created ByChannel:" + context.__name__ 
        transaction.get().note(note)
        args = baseArgs.copy()
        args ['channelId'] = youTubeId
        args ['part'] = 'snippet'
        results =  core (args,search,parseChannel)
        self.processResults (context,results)

def playListSearch(args):
        search_response = youtube.playlistItems().list(**args)
        search_response = search_response.execute()
        return search_response
    
class ByPlayList(Base):                      
    def __init__(self,view,youTubeId):
        context = view.new
        note =  "Created PlayList:" + context.__name__ 
        transaction.get().note(note)
        args = baseArgs.copy()
        args ['playlistId']=youTubeId       
        args ['part']= 'snippet,contentDetails'            
        results = core (args,playlistSearch,parsePlaylist)
        self.processResults (context,results)
        
def playListSearch(args):
        search_response = youtube.playlistItems().list(**args)
        search_response = search_response.execute()
        return search_response
    
class BySearchTerm(Base):                      
    def __init__(self,view,query):
        context = view.new
        note =  "Created Search:" + context.__name__ 
        transaction.get().note(note)
        args = baseArgs.copy()
        args ['q']=query
        args ['part']= 'snippet'
        args ['type']= 'video'
        #args ['videoDuration']= 'medium'
        args ['relevanceLanguage']= 'pl'                
        
        results =  core (args,search,parseChannel)        
        self.processResults (context,results)   

        #AND NOW FOR SHORT VIDEOS
        #del args ['pageToken']
        #args ['videoDuration']= 'medium'        
        #results =  core (args,search,parseChannel)        
        #self.processResults (context,results)           
