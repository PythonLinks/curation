from BTrees.OOBTree import OOBTree
from cromlech.browser.exceptions import HTTPFound

from zopache.pages.interfaces import IRecent, IPage
import heapq
import math
import arrow
import time

"""
So what do we have here?
There are six different caches.  3 for categories, 3 for videos. 
They are dictionaires indexed by item key. 
The 2 score caches for ideos.   wilson score and most recent.
Noo need to cache creation date.

The 3 for categories cache the __name__ of the top 10 videos in that
branch of the tree. 


The cache disappears everytime the app is restarted.
We only cache the results that someone has asked for. 
Cache is accessible from multiple threads. 
Caches will also be deleted upon edits. 

I do ont want to sort huge lists of objects, so I use heapq 
to just keep track of the 10 best items in any category. 
So sorting scales linearly with branch size, not n log (n)

The heapq sort uses a tuple 
(score, __name__, item)
That way two items with the same score can be compared by alphabetic name. 
Comparing the items gave an error. 
"""

import inspect
from functools import wraps


class Cache:

    def __init__(self):
            self.resetCache()

    def resetCache(self):
            self.wilsonScoreBest = {}
            self.myScoreBest = {}
            self.mostRecentBest = {}
            self.wilsonScoreCache = {}
            self.myScoreCache = {}

    def get(self, name, key, default=None):
            cache = getattr(self, name)
            return cache.get(key, default=default)

    def set(self,name, key, value):
            cache = getattr(self, name)
            cache[key] = value

    def clear(self, name, key, value):
            cache = getattr(self, name)
            if key in cache:
               del cache[key]
               return True
            return False

    def __call__(self, name):
            cache = getattr(self, name)
            def caching(func):
                @wraps(func)
                def cached(target,*args, **kwargs):
                    key = target.__name__
                    if key in cache:
                        value = cache.get(key)
                        if isinstance(value, list):
                              items = target.convertNamesToObjects(value)
                              return items
                        return value  
                    value = func(target,*args, **kwargs)
                    if isinstance(value, list):
                         names = target.convertObjectsToNames(value)           
                         cache[key] = names
                    else:
                         cache[key] = value
                    return value
                return cached
            return caching


cache = Cache()




class PageMixIn(object):
    
    #USED TO DISPLAY CHILDREN, BUT NOT HTML OBJECTS
    def childCategories(self):
        result =[]
        for item in self.values():
            if IPage.providedBy (item):
               result.append (item)
        return result
    
    #The best caches have to cache __name__
    #So we have to convert back and forth to ids. 
    def convertNamesToObjects(self,list):
       root = self.getRoot() 
       result = []
       for item in list:
           theItem = root.get (item)
           if theItem is not None:
              result.append(theItem)
       return result
   
    def convertObjectsToNames(self,list):
       result = []
       for item in list:
               result.append(item.__name__)
       return result
   
    @cache('wilsonScoreBest')           
    def bestWilsonScore(self):
        return self.bestObjects('wilsonScore')

    @cache('myScoreBest')               
    def bestMyScore(self):
        return self.bestObjects('myScore')

    @cache('mostRecentBest')               
    def bestMostRecent (self):
        return self.bestObjects('mostRecent')        

    def bestObjects(self,sortKey):
        root = self.getRoot()
        aHeap = []
        #FOR A CONFERENCE JUST COMPARE THE CONFERENCE TALKS
        isConference = (self.webClass == 'Conference')       
        if (isConference):
            self.bestConferenceObjects(sortKey,root,aHeap)
        else:
            self.bestCategoryObjects(sortKey,root,aHeap)
        result = []
        while (aHeap):
           result.append(heapq.heappop(aHeap)[2])
        result.reverse()
        return result

    #FOR A CATEOGRY
    def bestCategoryObjects(self,sortKey,root,aHeap):
       #FOR NON CONFERENCE CALCULATE THE BEST IN THIS BRANCH
       for item in self.values():
           if IRecent.providedBy(item):
              item.addToHeapQ2(aHeap,sortKey)
           if IPage.providedBy (item):
              item.bestCategoryObjects(sortKey,root,aHeap)

    #FOR A CONFERENCE
    def bestConferenceObjects(self,sortKey,root,aHeap):
       #FOR NON CONFERENCE CALCULATE THE BEST IN THIS BRANCH
       items =  list(map(lambda x: x, self.talks.items()))       
       
       for key,item in items:
           name = item.__name__
           if name  == None:
              item.__name__ = key
              del self.talks [key]
              continue
           if name != key:
              del self.talks [key]
              continue
           if IConferenceVideo.providedBy(item):
              item.addToHeapQ2(aHeap,sortKey,isConference = True)

       
class RecentMixIn(object):
    publishedAt = 0
    def addToHeapQ2(self,aHeap,sortKey, isConference = False):
        # For conferences we want to compare all the talks
        # Otherwise just the top 10
        if ((not isConference) and (len(aHeap)> 9)):
            heapq.heappushpop(aHeap,(getattr(self,sortKey),self.__name__,self))
        else:
            try:
               heapq.heappush(aHeap,(getattr(self,sortKey),self.__name__,self))
            except:
               pass
           
    @cache('wilsonScoreCache')                       
    def getWilsonScore (self):
                ups = self.upVotes()
                downs = self.downVotes()
                n = ups + downs
                if n == 0:
                    return 0
                z = 1.96 #1.44 = 85%, 1.96 = 95%
                phat = float(ups) / n
                wilsonScore = ((phat + z*z/(2*n) - z * math.sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n))
                #print (ups,' ',downs)
                #print (wilsonScore,' ',self.title)
                #import pdb; pdb.set_trace()
                return wilsonScore
            
    @cache('myScoreCache')                                   
    def getMyScore(self):
        viewCount = self.viewCount
        if viewCount == 0:
            return 0
        myScore =  1000*(self.upVotes() - (5 * self.downVotes()))/viewCount
        #print (self.upVotes(),' ',self.downVotes(),' ',self.viewCount)
        #print (myScore,' ',self.title)
        #import pdb; pdb.set_trace()
        return myScore

    def getMostRecent(self):
        if hasattr(self,'publishedAt'):
           return self.publishedAt
        else:
           print (self.title) 
           return 0
       
    def age(self):
       return arrow.get(self.creationTime).humanize()[:-3]
   
    def editDateForRSS(self):
        return time.strftime("%a, %d %b %Y %H:%M:%S %z",
                time.localtime(self.modificationTime))

    def humanCreationDate(self):
        if (self.publishedAt == 0):
            return '-'
        return time.strftime("%Y-%m-%d",time.localtime(self.publishedAt))

    def getDefaultThumbNailURL(self):
        try:
            return self.thumbnails.get('default').get('url')
        except:
            pass
        return ""
        
    def getSrcSet(self):
        if not hasattr(self,'thumbnails'):
            return ""
        values =  self.thumbnails.values()
        result = []
        for i in values:
            try:
               aString = (i['url'] + ' ' +
                          str(i['height']) + 'h ' +
                          str(i['width']) + 'w')
               result.append(aString)
            except:
                pass
        srcset = ",".join(result)
        return srcset          

                            
    mostRecent = property (getMostRecent)
    wilsonScore = property (getWilsonScore)
    myScore = property (getMyScore)


    
    def moveTo (self,view):
        request = view.request
        principal = request.principal
        if (principal.__name__ != 'lozinski'):
           return 'You are not authorized to move Videos'
        if not 'target' in request.form:
           return 'You have to define where to move the video.'
        targetName = request.form ['target']
        root = self.getRoot()
        try:
           newParent = root [targetName]
        except:
            return "That is not a valid destination anme for the video"
        name = self.__name__

        # YOU HAVE ALREACY CHECKED SCRUITY
        # SO PROCESS IT
        
        del self.__parent__ [name]
        newParent [name] = self
        raise HTTPFound(location='/' +targetName  + '/manage')

     
    
    def upVote(self,principal):
        self.possiblyCreateVoteCounts()
        key = principal.__name__
        if key in self._downVotes:
            del self._downVotes[key]
        if key in self._upVotes:
            del self._upVotes[key]
            return
        self._upVotes[key] = time.time()


    def downVote(self,principal):
        self.possiblyCreateVoteCounts()
        key = principal.__name__
        if key in self._upVotes:
            del self._upVotes[key]
        if key in self._downVotes:
            del self._downVotes[key]            
            return
        self._downVotes[key] = time.time()           
        
            
    def possiblyCreateVoteCounts(self):    
        if not hasattr(self,"_upVotes"):
           self._upVotes = OOBTree()
        if not hasattr(self,"_downVotes"):
           self._downVotes = OOBTree()           
        
        
