import sys
from datetime import datetime
 
timestamp = datetime.now().timestamp()
from BTrees.OOBTree import OOBTree

from cromlech.security import permissions

from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.pages.interfaces import ICategory
from discord_webhook import DiscordWebhook, DiscordEmbed

class Base(object):
    def processOne(self,unixTime,article,node):
      for aHook in node.webhooks.values():
           if self.wasSent(article, aHook.serverId ):
               continue
           webHook = DiscordWebhook(url = aHook.webHookURL)
           remoteURL = (getattr(article,'articleURL','') or
                     getattr(article,'remoteURL',""))
           webHook.timeout = 4
           description = article.description + " " + remoteURL
           #description += "\n via UncensoredNews.US"
           embed = DiscordEmbed(title = article.title,description = description)

           authorName, authorURL, authorLogo = article.getAuthor(self)
           embed.set_author(name = authorName,
                            url = authorURL,
                            icon_url = authorLogo )
           
           webHook.add_embed(embed)

           imageURL = self.secureShortURL(context = article) + "/Logo"
           embed.set_image(url=imageURL)
           try:
               response = webHook.execute()
           except :
              err = sys.exc_info()[0]
              self.status += str(err)
           self.recordSending(unixTime,article, aHook.serverId)
           self.status += (" " + aHook.channelName + " " +
                         article.title + "<br>" )
           Form.update(self)

@form_component
@context(ICategory)
@target(IView)
@name("webhooks")
@permissions('Manage')
class WebHook(Form,Base):
    title = "Send By Webhook"
    subTitle = "For the newest approved articles publishes them."
             
    def update(self):
      context = self.context

      for article in values:
        for ancestor in article.ancestors():
          if hasattr(ancestor, 'webhooks'):
            self.processOne(article, ancestor)


@form_component
@context(ICategory)
@target(IView)
@name("once")
class Once(Form,Base):
    title = "Post One Article Per Hook"
    subTitle = "Generate some motion"

    def update(self):
      context = self.context
      dateTimeNow = datetime.now()
      unixNow = dateTimeNow.timestamp()


      #Do Nothing in the middle of the night              
      if  0 < dateTimeNow.hour < 10:
          return
      
      for category in self.context.allCategoryObjects():
          if not hasattr(category, "webhooks"):
             continue 
          for hook in category.webhooks.values():
              serverId = hook.serverId 
              articles  = category.hours24ApprovedArticles(unixNow)
              publish, relevantArticle =  self.publishOrNot(unixNow,
                                                         articles,
                                                         serverId)
              print (category.title)
              breakpoint()
              if publish:
                  self.processOne(unixNow,relevantArticle, self.context) 
              else:
                  self.status += category.title +  " NO ARTICLES" +"<br>"


    def publishOrNot(self,unixNow, articles,serverId):
        yesterday = unixNow - 24 *3600
        availableArticles = []
        publishedArticles = []
        for item in articles:
            if self.wasSent(item,serverId):
               publishedArticles.append(item)
            else:
               availableArticles.append(item) 
        if len(availableArticles) == 0:
                return False,None
        if len(publishedArticles) == 0:
                return self.findArticleOnlyInThisCategory(availableArticles,
                                                          serverId)
        #Frequency in Hours   
        frequency =   (24-10) / len(availableArticles)
        publishedAt = publishedArticles[-1].sentTo[serverId] 
        if (unixNow - publishedAt) > frequency :
               return self.findArticleOnlyInThisCategory(availableArticles,
                                                         serverId)     
        return False, None    

    def findArticleOnlyInThisCategory (self,availableArticles,serverId):
        context = self.context
        for article in availableArticles:
            for category in article.ancestorsExcludingSelf():
                if category.__class__.__name__ != "Category":
                    continue
                if category == context:
                    return True, article
                if hasattr(category, "webHooks"):
                   for hook in category.webHooks.values():
                       if hook.serverId == serverId:
                          return False, None
        return False, None       
       
        
    
    def wasSent(self,article, to):
        if hasattr(article,'sentTo'):
           sentTo = article.sentTo
           for item in sentTo:
               if type(item) == str:
                  del article.sentTo
                  return False
           if to in sentTo:
               return True
        return False

    def recordSending (self,unixTime,article,to):
        if not hasattr(article, 'sentTo'):
           article.sentTo = OOBTree()
        article.sentTo[to] = unixTime




