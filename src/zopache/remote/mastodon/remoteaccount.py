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
    lastImported = 0
    
    def __init__(self):
         Source.__init__(self)
         self.reset()

    def previousImportTime(self,time,view):
            while True:
                time -= 1
                if - time not in view.contentByTime:
                    return time
            raise Exception("No Possible times were found!")

    def setMaxId(self, maxId,tootId):
        if maxId == None:
            return  tootId
               
        elif tootId <= maxId:
            return  tootId

        else:
            raise Exception("Something strange with the Mastodon Ids. ")
         
    def crawl(self,view):
        proxy = view.proxy
        startTime = view.startTime
        proxy = view.proxy
        account = self
        accountName = account.mastodonId
        logger.info("Crawling " + accountName )
        user = proxy.account_search(accountName)[0]
        pageCount = 0
        totalNewArticles = 0
        oldestTootAge = 0
        pageOfToots = [None]

        if self.crawledToStart == False: #first import
            maxId = self.maxId
            totalNewArticles = 0
            first = True
            logger.info("Crawling Old Toots ",
                          self.mastodonId)
            while pageOfToots and (proxy.ratelimit_remaining > 3):
                first = False
                pageOfToots = proxy.account_statuses(user.id,
                       max_id=maxId,
                       limit=1000)
                if len(pageOfToots) == 0:
                    self.crawledToStart = True
                    logger.info ("Crawled To Start", self.mastodonId)
                else:
                    oldestTootAge,maxId, newArticles = (
                      self.processPage(pageOfToots,view))
                    totalNewArticles += newArticles
                    pageCount += 1

            
        else:
            maxId = None
            oldestTootAge = 0
            first = True
            logger.info("Crawling Recent Toots " +  self.mastodonId)
                          
            while (pageOfToots and
                (proxy.ratelimit_remaining > 3) and
                (oldestTootAge < 6)):
                logger.info ("First Loop") 

                lastImported = account.lastImported
                lastImportedAgo = startTime - lastImported
                daysImportedAgo = lastImportedAgo/secondsInaDay
                #If last imported less than a day ago, only import
                #a day's toots. 
                if ((oldestTootAge > 1) and
                    (lastImportedAgo < secondsInaDay)):
                   logger.debug("Break: Only crawling for a day " +
                                 self.mastodonId) 

                   break
               
                pageOfToots = proxy.account_statuses(
                    user.id,
                    max_id = maxId)
                    
                if len(pageOfToots) == 0:
                    logger.warning("Stange, No Toots were returned ",
                          self.mastodonId)
                    break
               
                if first:
                    mostRecentTootId = pageOfToots [0].id                
                    if mostRecentTootId == self.mostRecentTootId:
                          logger.info("No New Toots ",
                          self.mastodonId)
                          break
                    #self.mostRecentTootId = mostRecentTootId
                    first = False 

                oldestTootAge,maxId, newArticles = (
                      self.processPage(pageOfToots,view))
                totalNewArticles += newArticles
                pageCount += 1
                self.maxId = maxId
        logger.info ("oldestToot Age %s",oldestTootAge)
        logger.info ("Imported Ago  %s",str(int(daysImportedAgo)))        
        
        if first == False:
            self.lastImported = startTime
            self.modificationTime = startTime
        self.maxId = maxId
        return totalNewArticles, pageCount

    def processPage(self,pageOfToots,view):
        view.allToots=allToots = set()
        view.newArticles = newArticles = {}
        view.oldArticles = oldArticles = set() 
        loopStart = time.time()
        self.processToots(pageOfToots,view)
        numberOfNewArticles = self.postProcessPage(view)

        loopEnd = time.time()
        loopTime = int(loopEnd - loopStart)
        lastToot = pageOfToots [-1]
        age = loopEnd - self.getPublicationTime(lastToot,view)
        oldestTootAge = int(age/(secondsInaDay))
        print ("Age = ", oldestTootAge," days", end = "")
        print("\nLoopTime = ", loopTime, " seconds")
        maxId = self.setMaxId(self.maxId,lastToot.id)
        return oldestTootAge,maxId, numberOfNewArticles
           
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
        for toot in pageOfToots:
           account = self
           message, new  = Toot().createToot(toot,account)
           print (message)
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

