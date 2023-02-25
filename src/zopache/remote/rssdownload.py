import aiohttp
import asyncio
import ssl
import time
import sys
import logging
from inspect import currentframe, getframeinfo

from dolmen.forms.base.markers import FAILURE, SUCCESS
from zopache.remote.irss import IRSSBase, IRSSArticle

logging.basicConfig(
   filename='/app/data/urls',
   filemode='w',
   format='%(message)s')

async def fetch(session,node,view):
   startTime = time.time()    
   duration =  0
   className = view.className(node)
   if className == "RSS":
      url = node.rssURL
   elif className == 'Article':
      if not node.title:
         url = node.articleURL
      else:   
         url = getattr(node,'imageURL',None)
         if url in ["",None]:
            return SUCCESS, (node.name + " No image URL.")
   elif className == "RSSArticle":
      url = getattr(node,'imageURL',None)
      if not url:
         return FAILURE, ("Existing Article " +
                          node.name +
                          " No image URL.") 
   else:
      return FAILURE, node.__name__, ("Error Trying to Fetch " +
      node.__class__.__name__)
   #NOW PROCESS THE URL
   try:
        url = url.strip()
        async with session.get(url) as response:
          status = response.status
          if status == 200:
             result = await node.processResponse(session,response,view)
             return  result
          else:
             statusStr = str(status) + ' '
             logging.warning(statusStr + url)
             return FAILURE,( node, 
                              ' status = ' +
                              statusStr +
                              url )
                              
   except asyncio.TimeoutError as err:
          duration =  time.time() - startTime
          duration = int(duration)
          return FAILURE, node, "TIME OUT: "  + str(duration) + 's ' + url
          
   except:
          frameinfo = getframeinfo(currentframe())
          e = sys.exc_info()[0]
          return (FAILURE,
                  (frameinfo.filename + ' ' +
                  str(frameinfo.lineno) + ' ' + 
                   str(e)),
                  node
                  )      
          return FAILURE, node ,  (" IN RSSDownload " +
                                   str(e) + ' ' + url) 

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
                                         'Article',
                                         'Toot'}:
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




