import time
import datetime

from apiclient.discovery import build
from apiclient.errors import HttpError
from zopache.categories.interfaces import ILightningTalk, IConferenceVideo

#There are two copies of this key
DEVELOPER_KEY = "AIzaSyAOHmZ91f6qIt6FTi5BdopElujsENSKeN0"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def getVotes(id):

  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  search_response = youtube.videos().list(
    part='snippet,statistics',      
    id=id ,
  ).execute()
  return search_response

#youtube_search("T-TwcmT6Rcw,Ks-_Mh1QhMc")
from pprint import pprint
def processVotes(response,byId):
  items = response['items']
  for item in items:
    snippet = item ['snippet']
    
    thumbnails = snippet ['thumbnails']
    #pprint (thumbnails)
    #print (snippet ['title'])
    publishedAt = snippet ['publishedAt']
    dt= datetime.datetime.strptime(publishedAt, '%Y-%m-%dT%H:%M:%S.%fZ')
    publishedAt = time.mktime(dt.timetuple())
    id = item ["id"]
    talk = byId[id]
    talk.publishedAt = publishedAt
    print (publishedAt, talk.title)
    talk.thumbnails = thumbnails
    talk._p_changed = True
    for key, value in item["statistics"].items():
      value = int (value)
      setattr(talk,key,value)

def recordVotes (context):
    byId ={}
    idArray = []
    for item in context:
       if hasattr(item, 'videoId'):
          videoId=item.videoId
          byId[videoId]=item
          idArray.append(videoId)
    
    i=0
    length = len(context)
    while (i*50 <= length-1 ):
          first = 50 * i
          last = min (first + 49, length)
          cut = idArray[first:last]
          string = ','.join(map(str,cut))
          votes=getVotes (string)
          i += 1
          print ("GOt BATCH ", i)
          processVotes(votes,byId)

from zopache.core.getroot import getSiteRoot
    
def recordLocalVotes(context):
      videos =[]
      for item in context.allBlogObjects():
          if (IConferenceVideo.providedBy(item) and not
             ILightningTalk.providedBy(item)):
              videos.append(item)
      recordVotes(videos) 


def getVideoDetails(context):
    recordVotes ([context])
    
def recordAllVotes(context):
      root = context.getSiteRoot()
      return recordLocalVotes(root)
    
          
