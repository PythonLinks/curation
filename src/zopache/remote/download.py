import aiohttp
import asyncio
import ssl
import time

count = []


async def fetch(url,allowedTime,startTime,processResponse):
   duration =  time.time() - startTime 
   print ("STARTING", duration,url)
   timeout = aiohttp.ClientTimeout(total=allowedTime)
   async with aiohttp.ClientSession(timeout = timeout) as session:
     try:  
        async with session.get(url) as response:
          if response.status != 200:
               return (response.status,url,'')      
          html  =  await response.text()
          duration =  time.time() - startTime
          print (len(count),"ENDING2", duration, url)
          count.append(1)
          return processResponse(url,html)
       
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
        responses = await fetch_all( urls,processResponse)
        results = {}
        for item in responses:
            print  (item [0], item [1])
            results [item[1]]=item [2]
        return results
               
def getResults(urls,processResponse):
   result = asyncio.run(fetchURLS(urls,processResponse))
   return result


if __name__ == '__main__':
   pass
