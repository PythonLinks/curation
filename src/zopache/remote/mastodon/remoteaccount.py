import time
import logging
import transaction

from dolmen.forms.base.markers import FAILURE
from zopache.core.viewdecorators import *
from zopache.remote.mastodon.toot import Toot
from zopache.remote.mastodon.interfaces import IRemoteAccount
from zopache.application.source import Source
from zopache.remote.rssdownload import fetchAll
from zopache.crud.getimage import getImage
from zopache.remote.news.article import Article
from zopache.core.transactionnote import TransactionNote


secondsInaDay = 3600 *24
crawlBackSeconds = secondsInaDay * 5 # Days

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(
    logging.FileHandler('/app/data/crawl', mode = "w"))


@implementer (IRemoteAccount)
class RemoteAccount(Source,TransactionNote):
    
    webClass = "RemoteAccount"
    htmlSummary = True
    title = ""
    twitterId = ''
    mastodonId = ''
    keepAllArticles = False
    wordsToAvoid = ""
    description = ""
    defaultCategory = ""
    domainName = ""
    maxId = None
    mostRecentTootId = None
    lastLongImportTime = 0
    
    def __init__(self):
         Source.__init__(self)
         self.reset()

    def previousImportTime(self,time,view):
            while True:
                time -= 1
                if - time not in view.contentByTime:
                    return time
            raise Exception("No Possible times were found!")



    def crawlingToStart (self,view,proxy,user):        
        maxId = self.maxId
        pageOfToots = [None]
        pageCount = 0
        totalNewArticles = 0
        logger.info("Crawling To Start " + self.mastodonId)
        while pageOfToots and (proxy.ratelimit_remaining > 3):
                pageOfToots = proxy.account_statuses(user.id,
                       max_id=maxId,
                       limit=1000)
                if len(pageOfToots) == 0:
                    self.crawledToStart = True
                    logger.info ("Crawled To Start" +  self.mastodonId)
                else:
                    existingToots, newArticles = (
                      self.processPage(pageOfToots,view))
                    totalNewArticles += newArticles
                    pageCount += 1
                lastToot = pageOfToots [-1]
                maxId = self.setMaxId(maxId,lastToot.id)
        self.maxId = maxId            
        return totalNewArticles, pageCount
    
    def setMaxId(self, maxId,tootId):
        if maxId == None:
            return  tootId
               
        elif tootId <= maxId:
            return  tootId

        else:
            raise Exception("Something strange with the Mastodon Ids. ")
         
    def crawl(self,view):
        proxy = view.proxy
        account = self
        accountName = account.mastodonId
        user = proxy.account_search(accountName)[0]
        logger.info ("\n---------------------------\n")
        if self.crawledToStart == False: #first import
               return self.crawlingToStart(view,proxy,user)
        else:
               return self.crawlingMostRecent(view,proxy,user)


    def crawlingMostRecent(self,view,proxy,user):           
        totalNewArticles = 0
        oldestTootAge = 0
        pageCount = 0
        maxId = None
        existingToots = False
        startTime = view .startTime
        lastLongImportTime = self.lastLongImportTime
        longImportedTimeAgo = startTime - lastLongImportTime
        daysLongImportedAgo = longImportedTimeAgo/secondsInaDay
        longImport = daysLongImportedAgo > 6 
        logger.info ("Imported Ago " +
                             str(int(daysLongImportedAgo)))
        if longImport == True:
            self.lastLongImportTime = startTime
            logger.info("Crawling Long Imports " +  self.mastodonId)       
        logger.info("Crawling Recent Toots " +  self.mastodonId)
        pageOfToots = proxy.account_statuses(
                              user.id,
                              max_id = maxId)
        if (len (pageOfToots) > 0):
            mostRecentTootId = pageOfToots [0].id                
            done = mostRecentTootId == self.mostRecentTootId
            if done:
                logger.info("No New Toots " + self.mastodonId)
                return 0, 0
            else:
                self.mostRecentTootId = mostRecentTootId
        self.lastImported = startTime
        self.modificationTime = startTime
                
        while (pageOfToots and
                (proxy.ratelimit_remaining > 3) ):
              if len(pageOfToots) == 0:
                  logger.warning("Stange, No Toots were returned ",
                          self.mastodonId)
                  break

              if (existingToots and
                  not longImport and 
                  (oldestTootAge > 1)):
                  logger.debug("Break: Only crawling for a day " +
                                 self.mastodonId) 
                  break
                       
              if (existingToots and
                  longImport and
                  (oldestTootAge > 6)):
                  logger.debug("Break: Crawled For 6 days  " +
                                 self.mastodonId) 
                  break                  

              existingToots, newArticles = (
                      self.processPage(pageOfToots,view))
              totalNewArticles += newArticles
              print ("TOTAL NEW ARTICLES + ", totalNewArticles)
              pageCount += 1
              lastToot = pageOfToots [-1]
              maxId = self.setMaxId(maxId,lastToot.id)
              oldestTootAge = self.tootAge(lastToot,view)
              print ("Age = ", oldestTootAge," days", end = "")
              pageOfToots = proxy.account_statuses(
                              user.id,
                              max_id = maxId)
                
        logger.info ("oldestToot Age " + str(int(oldestTootAge)))
        return totalNewArticles, pageCount

    def processPage(self,pageOfToots,view):
        view.allToots=allToots = set()
        view.newArticles = newArticles = {}
        view.oldArticles = oldArticles = set() 
        loopStart = time.time()
        existingToots = self.processToots(pageOfToots,view)
        numberOfNewArticles = self.postProcessPage(view)
        loopEnd = time.time()
        loopTime = int(loopEnd - loopStart)
        print("\nLoopTime = ", loopTime, " seconds")
        logger.info("Number of New Articles = " +
                    str(numberOfNewArticles ))
        if existingToots:
           logger.info("ExistingToots")
        return existingToots,  numberOfNewArticles
    
    def tootAge(self,toot,view):
        currentTime = view.startTime
        age = currentTime - self.getPublicationTime(toot,view)
        tootAge = int(age/(secondsInaDay))
        return tootAge
    
    def postProcessPage(self,view):
           allToots = view.allToots
           newArticles = view.newArticles
           oldArticles = view.oldArticles
           #Until you successfull fetch the article, 
           #and add it to the
           #Parent, it will not be in contentByTime. 
           for item in newArticles.values():
                  del view.contentByTime[-item.importTime]
           allArticles = set(newArticles.values()) | oldArticles
           self.fetchArticles (allArticles,view)
           for toot in allToots:
               for url in toot.articleURLs:
                   article = view.root.existsRemoteURL(url)
                   if article != False:
                      toot.addArticle(article) 
                      article.addToot(toot)
                      
           #Since the created articles did not know about
           #the relevant toots.
           root = view.root
           numberOfNewArticles = 0
           for article in newArticles.values():
               if article.name:
                   numberOfNewArticles += 1
                   root.unIndexItem(article)
                   root.indexItem(article)
           self.describeTransactionWithText(
                "Fetching from: " + self.mastodonId
           )                   
           transaction.manager.commit()
           return numberOfNewArticles

    #COPY OF THIS HERE AND IN RSS.PY    

    def fetchArticles(self,articles,view):
        result = fetchAll(articles,view, allowedTime = 20)
        for item in result:
            if item[0] ==  FAILURE:  
               view.submissionErrors.append("ERROR: " + str(item[1:]))
               if not 'status' in str(item[1:] ):
                  if not "TIME OUT" in str(item): 
                     try:
                         logger.warning ("\n" +  str(item))
                     except:
                         logger.warning ("\n" + str( type(item)))
                         
        view.status='RSS Feeds were downloaded.'

        
    def processToots(self,pageOfToots,view):
        root = view.root
        allToots = view.allToots
        newArticles = view.newArticles
        oldArticles = view.oldArticles
        contentByTime = root.contentByTime
        existingToots = False
        for toot in pageOfToots:
           account = self
           message, new  = Toot().createToot(toot,account)
           #logger.info (message)
           #try:
           #   print (message, new.title)
           #except:
           #   print (message)
           if message == "Existing Toot":
              existingToots = True
           if message != "SUCCESS":
               continue
           allToots.add(new)           
           for url in new.articleURLs:
               article = root.existsRemoteURL(url)
               if article == False:
                 if url not in newArticles:
                     anArticle = Article(toot,
                                       url,
                                       account,
                                       view.mastodonArticles,
                                       root)
                     importTime = self.getPublicationTime(toot,view)
                     importTime = self.previousImportTime(importTime,view)
                     anArticle.importTime = importTime
                     newArticles[url] = anArticle
                     contentByTime[-importTime] = anArticle
                     print(".", end = "") 
               else:                    
                   if not article.publicationApproved:
                       article.publicationApproved = True
                       oldArticles.add (article)
        return existingToots
    
    def getPublicationTime(self,toot,view):           
        try:
            publicationTime = time.mktime(toot.created_at.timetuple())
        except:    
            publicationTime = view.startTime
        return int (publicationTime)

         
    def valuesAsList(self):
        result = []
        for item in self.values():
               result.append (item)
        return result
         
    def reset(self):
         self.crawledToStart = False
         self.minId = None 
         self.maxId = None
        
    @property
    def remoteURL(self):
        blank,user, server = self.parts()
        return 'https://' + server + '/@' + user

    def parts(self):
        id = self.mastodonId
        if id[0]!='@':
            id = '@' + id
        return id.split('@')

    def userName(self):
        return "@" + self.parts()[1]
    
    def postAddProcess(self,view = None):
        if self.logoURL:
            getImage(self,self.logoURL)


class MastodonAccount(RemoteAccount):
    pass

import crom
from zopache.zmi.interfaces import IURLSegment
@crom.adapter
@crom.sources(IRemoteAccount)
@crom.target(IURLSegment)
class IRemoteAccountAdaptor(object):
    def __init__(self,context):
        self.context=context   

    def getSegment(self):
        return 'manage'

