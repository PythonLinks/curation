import json
from slugify import slugify

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
