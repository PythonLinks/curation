import aiohttp
import asyncio
import ssl
import time
from zopache.remote.rss import IRSSBase
from zopache.remote.rssarticle import IRSSArticle

async def fetch(node,allowedTime,startTime,view):
   duration =  time.time() - startTime 
   timeout = aiohttp.ClientTimeout(total=allowedTime)

   if IRSSBase.providedBy(node):
      url = node.rssURL
      print ("URL IS  AN RSS FEED " + node.name)      
   elif IRSSArticle.providedBy(node):
      if  'Logo' in node:
         return None
      url = node.getImageURL()
      if url == "":
         url = node.articleURL
         print("URL is An Article " + node.name)
      else:
         print ("URL is  an Image " + node.name)
      
   async with aiohttp.ClientSession(timeout = timeout) as session:
     try:
        async with session.get(url) as response:
          if response.status == 200:
             print ("FETCHING THE URL " + node.name)
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

tasks = []     
def fetchAll(nodes,view):
   return  asyncio.run(fetchCore(nodes,view))

async def fetchCore(nodes,view):   
    allowedTime = 40
    startTime = time.time()    
    for node in nodes:
        print ("Starting " + node.name)
        task = asyncio.create_task(fetch(node,
                                         allowedTime,
                                         startTime,
                                         view))
        tasks.append(task)
    return await asyncio.gather(*tasks)




