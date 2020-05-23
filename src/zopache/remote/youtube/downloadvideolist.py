#THIS DOWNLAODS THE DATA FOR CREATING A LIST OF VIDEOS. 
from pprint import pprint

def core(args,search,parse):

    videos = []
    data = search(args)
    videos, pageToken = parse(data,videos)
    total = 0
    while ( (pageToken !='') and
            (len (videos) < 101) ):
       args ['pageToken'] = pageToken
       data = search(args)
       new = len(data['items'])
       print (new)
       total += new
       videos, pageToken = parse (data,videos)   
       #print ('Total', total)
       #import pdb; pdb.set_trace()
       pass
     
    for item in videos:
        #print ()
        title = item ['title']
        #if ('|' in title):
        #   title = title.split('|')[0]
        #item['title']= title   
        #print (item['videoId'], ' '
        #print (item['title'])
        #print (item['description'])
        print ('LENGTH = ', len(videos))
    return videos

