import aiohttp
import asyncio
import feedparser

from pprint import pprint as pp

import time
start_time = time.time()

async def fetch(url):
   duration =  time.time() - start_time 
   print ("STARTING", duration,url)
   timeout = aiohttp.ClientTimeout(total=20)
   async with aiohttp.ClientSession(timeout = timeout) as session:
     try:  
        async with session.get(url) as response:
          if response.status != 200:
               return (response.status,url)      
          html  =  await response.text()
          duration =  time.time() - start_time 
          print ("ENDING", duration, url)
          #result = feedparser.parse(html)                
          #return  (result ,url)
          return  (html ,url)          
     except (asyncio.TimeoutError):
          return ("timeOut",url)
         


async def fetch_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(fetch(url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


urls = ['http://cnn.com',
            'http://google.com',
            'https://pythonlinks.info/doesnotexist'
            'http://twitter.com']

urls  = [
    "https://menarehuman.com/category/all/feed",
    "https://menarehuman.com/category/all/fixing-the-fight/rss",
    "https://menarehuman.com/category/all/mens-health-crisis/feed",
    "https://menarehuman.com/category/all/mrm/feed",
    "https://menarehuman.com/category/all/mens-health-crisis/feed",
    "https://menarehuman.com/category/all/mrm/feed",
    "https://menarehuman.com/category/all/our-stories/feed"]



async def fetchURLS(urls):    
        session = None
        htmls = await fetch_all(session, urls)
        for item in htmls:
            if isinstance(item[0], int):
                print (item)
            elif item[0]=="timeOut":
                print (item)                
            else:
                print (item[1])


if __name__ == '__main__':
    asyncio.run(fetchURLS(urls))
