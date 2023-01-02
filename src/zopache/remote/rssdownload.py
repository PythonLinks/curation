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
   if node.__class__.__name__ == "RSS":
      url = node.rssURL
   elif node.__class__.__name__ == "TootedArticle":
      if node.title == "":
         url = node.articleURL
      else:
         url = node.imageURL
   elif node.__class__.__name__ == "RSSArticle":
      return FAILURE, (node.__name__ + """We do not bulk
      download rssarticle nor their images.""")
   else:
      return FAILURE, node.__name__, ("Error Trying to Fetch " +
      node.__class__.__name__)

   #NOW PROCESS THE URL
   try:
        async with session.get(url) as response:

          if response.status == 200:
             result =   await node.processResponse(session,response,view)
             return SUCCESS, result
          else:
             return FAILURE, node.name, 'status = ' + str(response.status)

   except asyncio.TimeoutError as err:
          duration =  time.time() - startTime 
          return FAILURE, node.__name__, "TIME OUT"  + str(duration)
          
   except:
          e = sys.exc_info()[0]
          return FAILURE, node.__name__, str(e)

def fetchAll(nodes,view,allowedTime = 120):
    loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetchCore(nodes,view,allowedTime))
   
async def fetchCore(nodes,view,allowedTime):   
    tasks = []
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




