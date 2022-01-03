import json
from zopache.pages.page import Page
from zopache.core.viewdecorators import *
from BTrees.IOBTree import IOBTree
from zopache.pages.interfaces import ICategory
from BTrees.OOBTree import OOBTree

from time import time
from datetime import datetime
from itertools import islice
from zopache.application.mergeiterator import mergeiterator

secondsInADay = 24*60*60
def cmp(arg1,arg2):
    return - arg1.importTime + arg2.importTime

@implementer (ICategory)     
class Category(Page):
    webClass = "Category"
    title = ""
    description = ""
    source = ""
    tags = ""
    childFeeds = 0
    json = ""
    html = ""
    
    def getHTML(self):
        return self.html
    
    def getVideos(self,view):
        lastImportTime = None        
        url = view.url()
        parts = url.split('videos')
        lastImportTime = int(time())
        if ((len(parts) >= 2) and
            (len(parts[1]) >0)):
               lastImportTime = parts[1][1:]
               lastImportTime = int(lastImportTime)
        result = []
        values = self.newestVideos.values(min = -lastImportTime,
                                            excludemin = True)
        for item in islice(values,6):
            result.append(item)
        if len (result) > 0:
            lastImportTime = result [-1].importTime
        else:
            lastImortTime = 0
        return result, lastImportTime
    
    def getVideosJson(self,view,indent = 2):
        result = []
        result, lastImportTime = self.getVideos(view)
        for item in result:
            result.append(
            {"title":item.title,
             "slug": item.name,
             "parentSlug": item.parent.name,
             "parentTitle":item.parent.title,
             "description": item.description,
             "importTime": item.importTime,
             "iFrame": item.getWideFrame()
             }
            )
        return json.dumps(result, indent = indent)

    def __init__(self):
       Page.__init__(self)
       self.reInit()

    def descendants(self):
        yield self
        for item in self.onlyChildCategories():
            yield item
            for child  in item.onlyChildCategories():    
                yield child.descendants()
        
        raise StopIteration
    
    def onlyChildCategories(self):
        for item in self.iterValues():
            if item.__class__ == Category:
                yield item
        raise StopIteration

    def onlyNewsItems(self):
        for item in self.iterValues():
            if item.__class__ in { Category,Link}:
                yield item
        raise StopIteration            

    def reInit(self):
       self.newestArticles = IOBTree()
       self.newestVideos = IOBTree()       
       self.newestLinks = IOBTree()       
       self.approvedArticles = IOBTree()       
       self.childFeeds = 0

    def todaysFeedArticles(self,midnight):
        return self.newestArticles.itervalues(min = - midnight,
                                              max = -midnight + secondsInADay,
                                                  excludemin = True)
    def rawHeadlines(self):
        articles = list (self.feedArticles())
        if len(articles) ==0:
               return 0, [] 
        lastImportTime = articles [-1].importTime
        return lastImportTime,articles
    
    def moreFeedArticles(self,lastImportTime,howMany = 6):
        result = self.feedArticles(lastImportTime,howMany = howMany)
        all = []
        for item in result:
            all.append(item)
        return all
    
    def feedArticles(self,lastImportTime = None, howMany = 6):
        if lastImportTime:
            lastImportTime = - lastImportTime
        articles = self.newestArticles.itervalues(min = lastImportTime,                                                 excludemin = True)
        result = islice(articles, howMany)
        return result

    #Check the rss feed does not break.
    def curatedHeadlines(self,count = 6):
        articles = self.mergedApproved(howMany = count)
        if len(articles) == 0:
           return 0, [] 
        lastImportTime = articles [-1].importTime
        return lastImportTime, articles

    def todaysApprovedArticles(self,midnight):     
        return  self.approvedArticles.itervalues(min = -midnight,
                                      max = -midnight + secondsInADay,
                                      excludemin = True)                              
    def mergedApproved(self, howMany = 6, lastImportTime = None):
        result = []
        exclude = False
        if lastImportTime:
            lastImportTime = - lastImportTime
            exclude = True
        articles = self.approvedArticles.itervalues(min = lastImportTime,
                                                    excludemin = exclude)
        links = self.newestLinks.itervalues(min = lastImportTime,
                                            excludemin = exclude)
        for item in mergeiterator(articles,links, cmp = cmp):
               if item == None:
                   break
               result.append(item)
               if len(result) > 5:
                   break
               
        #if lastImportTime and len(result) > 0:
        #    result = result [1]
        return result

    #GET MORE APPROVED ARTICLES AFTER THE LAST IMPORT TIME
    def moreMergedApproved(self,lastImportTime,howMany = 6):
        try:
            
           result =  self.mergedApproved(lastImportTime = lastImportTime,
                                         howMany = howMany)
           return result
           
        except StopIteration:
           return []
        except Exception as err:
            print (err)

from zopache.pages.interfaces import (IGeographicalCategory,
                                      ILocationCategory,
                                      IRegionCategory,
                                      IMapCategory)

from zopache.pages.location import LocationContainer, MapBase

@implementer(ILocationCategory)
class LocationCategory(Category,LocationContainer):
    webClass = "LocationCategory"
    def mapPoints(self):
        return []
    
@implementer(IMapCategory)
class MapCategory(Category,MapBase):
    webClass = "MapCategory"
    def mapPoints(self):
        for child in self.values():
            if ILocationCategory.providedBy(child):
                yield child
            elif IRegionCategory.providedBy(item):                
                for grandChild in child.mapPoints():
                    yield grandChild
                yield child    

@implementer(IRegionCategory)
class RegionCategory(Category,MapBase):
    webClass = "RegionCategory"    
    def mapPoints(self):
        for child in self.values():
            if ILocationCategory.providedBy(child):
                yield child

    
