import aiohttp
import asyncio
import ssl
import time
import feedparser

count = []

def processImageResponse(url,response):
          print (url)
          return  ('Success' ,url,response)

def processRSSResponse(url,html):
          print (html[: 10])
          feed = feedparser.parse(html)
          entries = feed['entries']
          print ("LEN",len(entries))
          print (type(entries))
          for article in entries:
               permaLink = article['id']
               print ("Perma",permaLink)
          return  ('Success', url, entries)


async def fetch(url,allowedTime,startTime,fetchType):
   print ("URL = ", url)       
   duration =  time.time() - startTime 
   print ("STARTING", duration,url)
   timeout = aiohttp.ClientTimeout(total=allowedTime)

   async with aiohttp.ClientSession(timeout = timeout) as session:
     try:  
        async with session.get(url) as response:
          if response.status != 200:
               return (response.status,url,'')
          if fetchType == "RSS":  
              html  =  await response.text()
          elif fetchType == "Images":
              html = await response.body()
          else:
              raise Exception("Please Define a Fetch Type")
          
          duration =  time.time() - startTime
          print (len(count),"ENDING2", duration, url)
          count.append(1)
          return processRSSResponse(url,html)
       
     except (asyncio.TimeoutError):
          duration =  time.time() - startTime 
          print ("TIME OUT", duration, url)
          return ("timeOut",url,'')
       
     except (aiohttp.client_exceptions.InvalidURL):
        result = ("InvalidURL",url,'')
        print (result)
        return result
       
     except (aiohttp.client_exceptions.ClientConnectorError):    
        result = ("Cannot Connect",url,'')
        print (result)
        return result
     
     except (aiohttp.client_exceptions.ServerDisconnectedError):    
        result = ("Server DisConnect",url,'')
        print (result)
        return result
     
     except (ssl.SSLError):    
        result = ("SSL ERROR",url,'')              
        print (result)
        return result

     except Exception as err:
        print ("other errror",err)
        result = ("Other err",url,'')
        print (result)
        return result
       
async def fetch_all(urls,fetchType):
    tasks = []
    count = len(urls)
    allowedTime = 2 + count
    startTime = time.time()

    for url in urls:
        task = asyncio.create_task(fetch(url,
                                         allowedTime,
                                         startTime,
                                         fetchType))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def fetchURLS(urls,fetchType):    
        session = None
        responses = await fetch_all( urls,fetchType)
        results = {}
        for item in responses:
            print  (item [0], item [1])
            results [item[1]]=item [2]
        return results

       
def getRSS(urls):
   fetchType = "RSS"
   result = asyncio.run(fetchURLS(urls,fetchType))
   return result

def getImages(urls):
   urls.fetchType = "Images"
   result = asyncio.run(fetchURLS(urls))
   return result


if __name__ == '__main__':
   pass
