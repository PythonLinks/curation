import aiohttp
import asyncio
import ssl
import time
import sys

from zopache.remote.irss import IRSSBase, IRSSArticle

async def fetch(session,node,view):
   startTime = time.time()    
   duration =  0
   if IRSSBase.providedBy(node):
      url = node.rssURL
   elif IRSSArticle.providedBy(node):
      url = node.getImageURL()
      if url == "":
         url = node.articleURL
   else:
      return node, "Neither Feed Nor RSS Article"
   try:
        async with session.get(url) as response:
          if response.status == 200:
             result =  await node.pgrocessResponse(session,response,view)
             return result
          else:
             return node.name, 'status = ' + str(response.status)

   except asyncio.TimeoutError as err:
          duration =  time.time() - startTime 
          return node.name, "TIME OUT"  + str(duration)
          
   except aiohttp.client_exceptions.InvalidURL as err:
          return node.name, str(err)
       
   except aiohttp.client_exceptions.ClientConnectorError as err:    
          return node.name, str(err)          
     
   except aiohttp.client_exceptions.ServerDisconnectedError as err:    
          return node.name, str(err)          
  
   except ssl.SSLError as err:    
          return node.name, str(err)          

   except:
          e = sys.exc_info()[0]
          return node.name, str(e)

   return node.name, "UNEXPlAINED ERROR"



def fetchAll(nodes,view):
    loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetchCore(nodes,view))
   
async def fetchCore(nodes,view):   
    tasks = []
    allowedTime = 120
    timeout = aiohttp.ClientTimeout(total=allowedTime)
    async with aiohttp.ClientSession(timeout = timeout) as session:    
      for node in nodes:
         if view.className(node) not in ['RSS','RSSArticle']:
            continue
         if IRSSArticle.providedBy(node):
              if  'Logo' in node:
                   continue
         task = asyncio.create_task(fetch(session,
                                         node,
                                          view))
         tasks.append(task)
      result = await asyncio.gather(*tasks)
    return result  




