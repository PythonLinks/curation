import aiohttp
import asyncio
import ssl

import time

count = []
allEntries = {}


async def fetch(url,allowedTime,startTime,processResponse):
   duration =  time.time() - startTime 
   print ("STARTING", duration,url)
   timeout = aiohttp.ClientTimeout(total=allowedTime)
   async with aiohttp.ClientSession(timeout = timeout) as session:
     try:  
        async with session.get(url) as response:
          if response.status != 200:
               return (response.status,url)      
          html  =  await response.text()
          duration =  time.time() - startTime
          print (len(count),"ENDING2", duration, url)
          count.append(1)
          print (html[: 10])
          return processResponse(html)
       
     except (asyncio.TimeoutError):
          duration =  time.time() - startTime 
          print ("TIME OUT", duration, url)
          return ("timeOut",url)
       
     except (aiohttp.client_exceptions.InvalidURL):
        result = ("InvalidURL",url)
        print (result)
        return result
       
     except (aiohttp.client_exceptions.ClientConnectorError):    
        result = ("Cannot Connect",url)
        print (result)
        return result
     except (aiohttp.client_exceptions.ServerDisconnectedError):    
        result = ("Server DisConnect",url)
        print (result)
        return result
     except (ssl.SSLError):    
        result = ("SSL ERROR",url)              
        print (result)
        return result
     except Exception as err:
        print ("other errror",err)
        result = ("Other err",url)
        print (result)
        return result
       
async def fetch_all(urls,processResponse):
    tasks = []
    count = len(urls)
    allowedTime = 2 + count
    startTime = time.time()    
    for url in urls:
        task = asyncio.create_task(fetch(url,
                                         allowedTime,
                                         startTime,
                                         processResponse))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def fetchURLS(urls,processResponse):    
        session = None
        htmls = await fetch_all( urls,processResponse)
        for item in htmls:
                print (item)
        return htmls

import feedparser
def processRssResponse(html):          
          feed = feedparser.parse(html)
          entries = feed['entries']
          print ("LEN",len(entries))
          print (type(entries))
          for article in entries:
               permalink = article['id']
               print ("Perma",permalink)
               allEntries [permalink]=article          
          return  ('Success' ,url)

               
def getResults(urls,processResponse):
   result = asyncio.run(fetchURLS(urls,processResponse))

   return allEntries

if __name__ == '__main__':
   pass
