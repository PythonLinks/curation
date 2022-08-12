import json
from time import time
from datetime import datetime
from itertools import islice

from BTrees.IOBTree import IOBTree
from BTrees.OOBTree import OOBTree
from ZODB.blob import Blob, BlobFile
from ZODB.POSException import POSKeyError

from dolmen.container import BTreeContainer

from zopache.application.mergeiterator import mergeiterator
from zopache.pages.page import Page
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import ICategory
from zopache.ttw.file import FileBase
from zopache.ttw.container import AdminContainer

secondsInADay = 24*60*60

class Base(object):    
    @property
    def size(self):
        return len(self.source)

    def setSource(self, data):
        if len(data) == 0:
            return
        if not hasattr(self,'blob'):
            self.blob = Blob()
        with self.blob.open(mode ="w") as blobFile:
           blobFile.write(data)
           
    def getSource(self):
        if not hasattr(self,'blob'):
            return self.default
        try:
            with  self.blob.open(mode='r') as f:
               return f.read()
        except POSKeyError as error:
            return error.args[0]

    source = property(getSource,setSource)

@implementer (ICategory)     
class Category(Page):
    webClass = "Category"
    title = ""
    description = ""
    source = """{"time":1641561523293,"blocks":[{"id":"2dz3jTLAim","type":"header","data":{"text":"Title (It has to be first and use H1)","level":1}},{"id":"xCIIjcsAVQ","type":"layout","data":{"itemContent":{"1":{"blocks":[{"id":"l_k1euDW-S","type":"paragraph","data":{"text":"item content 1"}}]}},"layout":{"type":"container","id":"demo-data-container","className":"demo-data-container","style":"border: 1px solid #000000; padding: 16px; ","children":[{"type":"item","id":"demo-data-item-1","className":"demo-data-item-1","style":"border: 1px solid #000000; display: inline-block; padding: 8px; ","itemContentId":"1"}]}}}],"version":"2.22.2"} """
    tags = ""
    childFeeds = 0
    json = "[]"
    html = ""
    articleApproved = False

    def __init__(self):
       Page.__init__(self)
       self.reInit()

    def reInit(self):
       self.childFeeds = 0

       #Soon the following can be removed. 
       if hasattr(self,'newestArticles'):
           del self.newestArticles        
       if hasattr(self,'approvedArticles'):
           del self.approvedArticles       
       if hasattr(self,'bestArticles'):
           del self.bestArticles       
       if hasattr(self,'newestVideos'):
           del self.newestVideos       
       if hasattr(self,'newestLinks'):
           del self.newestLinks


    def get(self, name,default=None):
        if name == "@webhooks":
            if not hasattr(self,'webhooks'):
                self.webhooks = AdminContainer()
                self.webhooks.__parent__ = self
                self.webhooks.__name__ = "@webhooks"
            return self.webhooks
        return Page.get(self,name,default = default)
    
    # Only invoke index and unindex when the web approved status is changed.
    # Maybe Predelete Also.
    
    def preProcess(self,view = None):
        view.oldWebApproved = self.webApproved

    def postProcess(self,view = None):
        if (self.webApproved == True) and (view.oldWebApproved == False):
           self.getSiteRoot().indexItem(self)
        elif (self.webApproved == False) and (view.oldWebApproved == True): 
           self.getsiteRoot().unIndexItem(self)
           
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

    def todaysFeedArticles(self,midnight):
        return self.newestArticles.itervalues(min = - midnight,
                                              max = -midnight + secondsInADay,
                                                  excludemin = True)
    def rawHeadlines(self, howMany = 6):
        articles = list (self.feedArticles(howMany = howMany))
        if len(articles) ==0:
               return 0, [] 
        lastImportTime = articles [-1].importTime
        return lastImportTime,articles
    
    def moreFeedArticles(self,lastImportTime,howMany = 6):
        result = self.feedArticles(lastImportTime,howMany = howMany)
        return list(result)
    
    def feedArticles(self,lastImportTime = None, howMany = 6):
        if lastImportTime:
            lastImportTime = - lastImportTime
        articles = self.newestArticles.itervalues(min = lastImportTime,                                                 excludemin = True)
        result = islice(articles, howMany)
        return result

    #Check the rss feed does not break.
    def curatedHeadlines(self,count = 6):
        articles = list(self.mergedApproved(howMany = count))
        if len(articles) == 0:
           return 0, [] 
        lastImportTime = articles [-1].importTime
        return lastImportTime, articles

    def bestHeadlines(self,count = 6):
        articles = list(self.best(howMany = count))
        if len(articles) == 0:
           return 0, [] 
        lastImportTime = articles [-1].importTime
        return lastImportTime, articles    

    def best(self, howMany = 6, lastImportTime = None):
        exclude = False
        if lastImportTime:
            lastImportTime = - lastImportTime
            exclude = True
        articles = self.bestArticles.itervalues(min = lastImportTime,
                                                    excludemin = exclude)
        result = islice(articles, howMany)
        return result
    
    def mergedApproved(self, howMany = 6, lastImportTime = None):
        exclude = False
        if lastImportTime:
            lastImportTime = - lastImportTime
            exclude = True
        articles = self.approvedArticles.itervalues(min = lastImportTime,
                                                    excludemin = exclude)
        result = islice(articles, howMany)
        return result

    def todaysApprovedArticles(self,midnight):     
        return  self.approvedArticles.itervalues(min = -midnight,
                                      max = -midnight + secondsInADay,
                                      excludemin = True)                           
    def hours24ApprovedArticles(self, unixNow):
        unixNow = int(unixNow)
        yesterday =  unixNow - (24 *3600)
        return  self.approvedArticles.itervalues(min = -unixNow,
                                      max = -yesterday,
                                            excludemin = False)
    
    #GET MORE APPROVED ARTICLES AFTER THE LAST IMPORT TIME
    def moreMergedApproved(self,lastImportTime,howMany = 6):
         return  self.mergedApproved(lastImportTime = lastImportTime,
                                         howMany = howMany)
    def moreBest(self,lastImportTime,howMany = 6):
         return  self.best(lastImportTime = lastImportTime,
                                         howMany = howMany)     

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

from zopache.zmi.interfaces import IURLSegment
import crom
@crom.adapter
@crom.sources(ICategory)
@crom.target(IURLSegment)
class ICategoryAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'manage'        
