import json
from slugify import slugify


def parseChannel(data, videos):

       try: 
          nextPageToken = data ['nextPageToken']
       except:
           nextPageToken = ''   
       items = data['items']
       for item in items:
              id = item['id']
              if id['kind']!='youtube#video':
                 continue
              video ={}
              videoId = id["videoId"]
              video ['videoId'] = videoId
              snippet = item['snippet']
              title =  snippet["title"].strip()
              video ['title'] = title
              description =  snippet["description"]
              video['description'] = description
              print ( snippet['publishedAt'])
              videos.append (video)
       return videos ,nextPageToken

def parsePlayList(data, videos):
       try: 
          nextPageToken = data ['nextPageToken']
       except:
           nextPageToken = ''   

       items = data['items']
       for item in items:
              video ={}
              videoId = item['contentDetails']["videoId"]
              video ['videoId'] = videoId
              title =  item ['snippet']["title"].strip()
              video ['title'] = title
              description =  item ['snippet']["description"]
              video['description'] = description
              videos.append (video)
       return videos ,nextPageToken
