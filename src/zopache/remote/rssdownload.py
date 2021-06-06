import aiohttp
import asyncio
import ssl
import time
from zopache.remote.rss import IRSSBase
from zopache.remote.rssarticle import IRSSArticle

async def fetch(session,node,startTime,view):
   duration =  time.time() - startTime 

   if IRSSBase.providedBy(node):
      url = node.rssURL
      #print ("URL IS  AN RSS FEED " + node.name)      
   elif IRSSArticle.providedBy(node):
      if  'Logo' in node:
         return None
      url = node.getImageURL()
      if url == "":
         url = node.articleURL
         #print("URL is An Article " + node.name)
      else:
         print ("URL is  an Image " + node.name)

   try:
        async with session.get(url) as response:
          if response.status == 200:
             #print ("FETCHED THE URL " + node.name)
             #print("IN DOWNLOAD  RETURNIng IMAge", node.name)             
             return await node.processResponse(response,view)
       
   except asyncio.TimeoutError as err:
          duration =  time.time() - startTime 
          print ("TIME OUT", duration, node.name)
          print (node.name,err)
          
   except (aiohttp.client_exceptions.InvalidURL):
          print (node.name,err)
       
   except (aiohttp.client_exceptions.ClientConnectorError):    
          print (node.name,err)
     
   except (aiohttp.client_exceptions.ServerDisconnectedError):    
          print (node.name,err)
     
   except ssl.SSLError as err:    
          print (node.name,err)


   except Exception as err:
          print (node.name,err)
          
   return None     


def fetchAll(nodes,view):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(fetchCore(nodes,view))
   
async def fetchCore(nodes,view):   
    tasks = []
    allowedTime = 40
    timeout = aiohttp.ClientTimeout(total=allowedTime)
    async with aiohttp.ClientSession(timeout = timeout) as session:    
      for node in nodes:
        startTime = time.time()    
        print ("Starting " + node.name)
        task = asyncio.create_task(fetch(session,
                                         node,
                                         startTime,
                                         view))
        tasks.append(task)
      result = await asyncio.gather(*tasks)
    return result  



<<<<<<< HEAD
if __name__ == '__main__':
   pass
=======

>>>>>>> ef56173d3c1a0bc32a067cfed31152cb85de0cb7
