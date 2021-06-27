from time import time
from datetime import datetime
from itertools import islice

secondsInADay = 24*60*60

class NewsMethods(object):

    def headlines(self):
        now = datetime.now().timestamp()
        articles = []
        days = 2
        while len(articles) < 6:
            midnight = self.midnight(now)
            lastImportTime = midnight
            approved = list(self.todaysCuratedArticles(midnight, days = days) )
            articles += approved
            feedArticles = self.todaysFeedArticles(midnight)
            while len(articles) < 6:

                try:
                   article = next(feedArticles)
                   lastImportTime = article.importTime
                   articles.append (article)
                except StopIteration:
                   if days == 2:
                      days = 0
                   else:
                       days = 1
                   midnight  -= secondsInADay
                   lastImportTime = midnight
                   now = midnight
                   approved = list(self.todaysCuratedArticles(midnight) )
                   articles += approved
                   feedArticles = self.todaysFeedArticles(midnight)
            return lastImportTime,articles


    def moreNews(self,lastImportTime,howMany = 6):        
        articles = []
        midnight = self.midnight(lastImportTime)
        tonight = self.midnight(datetime.now().timestamp())
        while len(articles) < howMany:
            more = list(self.feedArticles(lastImportTime,limit = howMany))
            for item in more:
              if len(articles) >= howMany:
                  break
              if self.midnight(item.importTime) == midnight:
                  articles.append(item)
              else:
                  midnight -= secondsInADay
                  lastImportTime = midnight
                  if  ( tonight - secondsInADay != midnight):    
                      approvedArticles = list(self.todaysApprovedArticles(
                          midnight))
                      articles = articles + approvedArticles
        return articles
   
    def midnight(self,time):
       midnight = datetime.fromtimestamp(time)
       midnight = midnight.replace(hour=0, minute=0, second=0, microsecond=0)
       midnight = midnight.timestamp()
       midnight = midnight + secondsInADay
       return midnight
   
    def todaysApprovedArticles(self,midnight):     
        return  self.approvedArticles.itervalues(min = -midnight,
                                      max = -midnight + secondsInADay,
                                      excludemin = True)                                      
    def todaysFeedArticles(self,midnight):
        return self.newestArticles.itervalues(min = - midnight,
                                              max = -midnight + secondsInADay,
                                              excludemin = True)
        
    def feedArticles(self,lastImportTime = None, limit = 100):
        if lastImportTime:
            lastImportTime = - lastImportTime
        articles = self.newestArticles.itervalues(min = lastImportTime,                                                 excludemin = True)
        result = islice(articles, limit)
        return result

    def todaysCuratedArticles(self, endTime, days = 1):
        beginTime = endTime - (days * secondsInADay)                                  
        articles = self.approvedArticles.itervalues(min = -endTime,
                                                max = -beginTime)
        links = self.newestLinks.itervalues(min = -endTime,
                                        max = -beginTime)
        both = list(articles) + list (links)
        both.sort(key=lambda x:-x.creationTime)
        return both

    def mergedApprovedDays(self, count = 10):
        return islice(self.mergedCore(),count)
    
    def mergedCore(self):    
        articles = self.approvedArticles.itervalues()
        links = self.newestLinks.itervalues()
        nextArticle =  next(articles)
        nextLink = next(links)
        articleTime = nextArticle.importTime
        linkTime = nextLink.importTime
        while (True):
          if articleTime >= linkTime:
            currentArticle = nextArticle 
            nextArticle = next(articles)
            articleTime = nextArticle.importTime
            yield currentArticle
          else:
            currentLink = nextLink
            nextLink = next(links)
            linkTime = nextLink.importTime
            yield currentLink
    
