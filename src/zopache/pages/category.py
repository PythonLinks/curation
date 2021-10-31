from zopache.pages.page import Page
from zopache.core.viewdecorators import *
from BTrees.LOBTree import LOBTree
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
    childFeeds = 0
    def __init__(self):
       Page.__init__(self)
       self.reInit()

    def reInit(self):
       self.newestArticles = OOBTree()
       self.newestLinks = OOBTree()       
       self.approvedArticles = OOBTree()       
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
        return self.feedArticles(lastImportTime,howMany = howMany)

    def feedArticles(self,lastImportTime = None, howMany = 100):
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
        if lastImportTime:
            lastImportTime = - lastImportTime
        articles = self.approvedArticles.itervalues(min = lastImportTime,
                                                excludemin = True)
        links = self.newestLinks.itervalues(min = lastImportTime,
                                           excludemin = True)
        for item in mergeiterator(articles,links, cmp = cmp):
               if item == None:
                   break
               result.append(item)
        return result

    #GET MORE APPROVED ARTICLES AFTER THE LAST IMPORT TIME
    def moreMergedApproved(self,lastImportTime,howMany = 6):
        try:
           return islice(self.mergedApproved(lastImportTime = lastImportTime),
                      howMany)
        except StopIteration:
           return []
    
