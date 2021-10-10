from time import time
from datetime import datetime
from itertools import islice

secondsInADay = 24*60*60

class NewsMethods(object):

    def todaysFeedArticles(self,midnight):
        return self.newestArticles.itervalues(min = - midnight,
                                              max = -midnight + secondsInADay,
                                                  excludemin = True)
    def rawHeadlines(self):
        articles = list (self.feedArticles())
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
    def curatedHeadlines(self,count = 10):
        articles = list(islice(self.mergedApproved(),count))
        lastImportTime = articles [-1].importTime
        return lastImportTime, articles

    def todaysApprovedArticles(self,midnight):     
        return  self.approvedArticles.itervalues(min = -midnight,
                                      max = -midnight + secondsInADay,
                                      excludemin = True)                           
    #GET MORE APPROVED ARTICLES AFTER THE LAST IMPORT TIME
    def moreMergedApproved(self,lastImportTime,howMany = 6):
        return islice(self.mergedApproved(lastImportTime = lastImportTime),
                      howMany)

    def mergedApproved(self, lastImportTime = None):
        if lastImportTime:
            lastImportTime = - lastImportTime        
        articles = self.approvedArticles.itervalues(min = lastImportTime,
                                                excludemin = True)
        links = self.newestLinks.itervalues(min = lastImportTime,
                                           excludemin = True)  
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


    def midnight(self,time):
       midnight = datetime.fromtimestamp(time)
       midnight = midnight.replace(hour=0, minute=0, second=0, microsecond=0)
       midnight = midnight.timestamp()
       midnight = midnight + secondsInADay
       return midnight
    """
    #AND HERE WE HAVE THE NO LONGER USED ALGORITHMS
    #FOR SHOWING BOTH APPROVED AND NEW ARTICLES                                    def mixedHeadlines(self, daysArg = 2):
        days = daysArg
        now = datetime.now().timestamp()
        articles = []
        while len(articles) < 6:
            midnight = self.midnight(now)
            lastImportTime = midnight
            approved = list(self.recentCuratedArticles(midnight, days = days) )
            articles += approved
            feedArticles = self.todaysFeedArticles(midnight)
            while len(articles) < 6:
                try:
                   article = next(feedArticles)
                   lastImportTime = article.importTime
                   articles.append (article)
                except StopIteration:
                   if days == daysArg:
                      days = 0
                   else:
                       days = 1
                   midnight  -= secondsInADay
                   lastImportTime = midnight
                   now = midnight
                   approved = list(self.recentCuratedArticles(midnight) )
                   articles += approved
                   feedArticles = self.todaysFeedArticles(midnight)
            return lastImportTime,articles

    #GET MORE APPROVED AND UNAPPROVED ARTICLES.
    #APPROVED FOR TODAY, FOLLOWED BY ALL FOR TODAY. 
    #STARTS WITH 2 DAYS OF APPROVED, 
    def moreMixed(self,lastImportTime,howMany = 6):        
        articles = []
        midnight = self.midnight(lastImportTime)
        tonight = self.midnight(datetime.now().timestamp())
        while len(articles) < howMany:
            more = list(self.feedArticles(lastImportTime,howMany= howMany))
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
    """
