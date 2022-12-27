import aiohttp
import asyncio
import ssl
import time
import sys

from dolmen.forms.base.markers import FAILURE, SUCCESS

from zopache.remote.irss import IRSSBase, IRSSArticle

async def fetch(session,node,view):
   startTime = time.time()    
   duration =  0
   if IRSSBase.providedBy(node):
      url = node.rssURL
   elif node.__class__.__name__ == "AToot":
      url = node.remoteURL
   elif IRSSArticle.providedBy(node):
      url = node.getImageURL()
      if url == "":
         url = node.articleURL
   else:
      return FAILURE, node.__name__, "Neither Feed Nor RSS Article"
   try:
        async with session.get(url) as response:
          if response.status == 200:
             result =  await node.processResponse(session,response,view)
             return SUCCESS, result
          else:
             return FAILURE, node.name, 'status = ' + str(response.status)

   except asyncio.TimeoutError as err:
          duration =  time.time() - startTime 
          return FAILURE, node.__name__, "TIME OUT"  + str(duration)
          
   except aiohttp.client_exceptions.InvalidURL as err:
          return FAILURE, node.__name__, str(err)
       
   except aiohttp.client_exceptions.ClientConnectorError as err:    
          return FAILURE, node.__name__, str(err)          
     
   except aiohttp.client_exceptions.ServerDisconnectedError as err:    
          return FAILURE, node.__name__, str(err)          
  
   except ssl.SSLError as err:    
          return FAILURE, node.__name__, str(err)
       
   except AttributeError as err:
          return FAILURE, node.__name__, str(err)                 

   except:
          e = sys.exc_info()[0]
          return FAILURE, node.__name__, str(e)

   return FAILURE, node.name, "UNEXPlAINED ERROR"

def fetchAll(nodes,view):
    loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetchCore(nodes,view))
   
async def fetchCore(nodes,view):   
    tasks = []
    allowedTime = 120
    timeout = aiohttp.ClientTimeout(total=allowedTime)
    user_agent = {'User-agent': 'Mozilla/5.0'}
    async with aiohttp.ClientSession(timeout = timeout,
                       headers = user_agent
                     ) as session:    
      for node in nodes:
         if view.className(node) not in {'RSS',
                                         'RSSArticle',
                                         'TootedArticle'}:
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




