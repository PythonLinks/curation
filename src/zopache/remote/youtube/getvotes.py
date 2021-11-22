#SO THIS FILE CAN RECORD VOTES OF THE WHOLE TREE, A BRANCH OFTHE TREE OR A SINGLE FILE. recordAllVotes, recordLocalvotes, getVideoDetails. 
#getVotes gets the data, process votes proceses the data, and recordVotes
#records the data. 

import time
import datetime

from apiclient.discovery import build
from apiclient.errors import HttpError
from zopache.core.interfaces import IVideo
from zopache.core.getroot import getPublicationRoot

#There are two copies of this key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def getYouTubeObject(context):
    siteRoot= getPublicationRoot(context)
    DEVELOPER_KEY = siteRoot.youTubeKey
    youTubeObject = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
    return youTubeObject
  
def getVotes(id,youTubeObject):
  search_response = youTubeObject.videos().list(
    part='snippet,statistics',      
    id=id ,
  ).execute()
  return search_response


from pprint import pprint
def processVotes(response,byId):
  items = response['items']
  for item in items:
    snippet = item ['snippet']
    thumbnails = snippet ['thumbnails']
    #pprint (thumbnails)
    #print (snippet ['title'])
    publishedAt = snippet ['publishedAt']

    dt= datetime.datetime.strptime(publishedAt, '%Y-%m-%dT%H:%M:%fZ')
    publishedAt = time.mktime(dt.timetuple())
    id = item ["id"]
    for talk in byId[id]:
        talk.publishedAt = publishedAt
        print (publishedAt, talk.title)
        talk.thumbnails = thumbnails
        talk._p_changed = True
        for key, value in item["statistics"].items():
           value = int (value)
           setattr(talk,key,value)

def recordVotes (listOfVideos,context):

    youTubeObject = getYouTubeObject(context)
    byId ={}
    for item in listOfVideos:
       if hasattr(item, 'videoId'):
          videoId=item.videoId
          if not videoId in byId:
                 byId[videoId]= []
          byId[videoId].append (item)
          continue
      
    idArray = list(byId.keys())
    i=0
    length = len(idArray)
    while (i*50 <= length-1 ):
          first = 50 * i
          last = min (first + 49, length)
          cut = idArray[first:last]
          string = ','.join(map(str,cut))
          votes=getVotes (string, youTubeObject)
          i += 1
          print ("GOt BATCH ", i)
          processVotes(votes,byId)

from zopache.core.getroot import getSiteRoot
from zopache.core.interfaces import IVideo

def recordLocalVotes(context):
      videos =[]
      for item in context.allBlogObjects():
          if IVideo.providedBy(item):
              videos.append(item)
      recordVotes(videos,context) 

def getVideoDetails(aVideo):
    context = aVideo
    recordVotes ([aVideo],context)
    
def recordAllVotes(context):
      root = context.getSiteRoot()
      return recordLocalVotes(root)
    
          
