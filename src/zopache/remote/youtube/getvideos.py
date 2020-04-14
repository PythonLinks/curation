from pprint import pprint


#id = "PLYx7XA2nY5Gd-tNhm79CNMe_qvi35PgUR" #SCIPY-2018
#id = "PLX7Eu6MEBYSJeOdWM-_9N8G-8Yp47Ce2E" #Windows Playlist
#id = "PLGB9meziqbzpoB9i8UcYMipexqdsMYutY" #AnacondaCon 18
#id = "PLGVZCDnMOq0oQh7daBKy1AW5Q34d0LDsC" #PyData Berlin 2018

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

