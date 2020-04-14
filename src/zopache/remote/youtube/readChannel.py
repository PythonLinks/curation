import json
from slugify import slugify
from dolmen.container import OrderedBTreeContainer
from zopache.core import Container, Leaf
from zopache.categories.category import ConferenceVideo

def readdata(context):
#def readdata():
    path ='/home/lozinski/code/cromlech/ZopacheDemo/src/zopache.categories/src/zopache/categories/youtube/'
    for name in ('file1','file2','file3'):
       fileName = path  + name
       file =  open(fileName,'r')
       data = file.read()
       file.close()
       json1 = json.loads(data)

       items = json1['items']
       for item in items:
           if 'channelId' in item['id']:
               continue
           if (True): 
              videoId = item['id']["videoId"]
              title =  item ['snippet']["title"]
              youTubeDescription =  item ['snippet']["description"]

              if title == 'PyCon 2018':
                 continue
              segments = title.split(' - ')
              if 'Lightning' in title:
                  title = segments[0] + ': ' + segments[1]
              if (len(segments) == 4):
                 title = segments[1] + ' - ' + segments [2]
              elif (len(segments) == 3):
                 title = segments[1]
              elif (len(segments) == 2):
                 title = segments[1]
              elif (len(segments) == 0):
                   title = "No TITLE GIVEN" 
              title = title.strip()
              author = segments [0]
              print (videoId, author, title)
              chat = ConferenceVideo()
              chat.title=title
              chat.videoId = videoId
              chat.youTubeDescription = youTubeDescription
              chat.source = ''
              chat.youTubeAuthor = author
              name = slugify (title)
              if not name in context:
                  context [name] = chat

#readdata()
