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
@permissions('Manage')
class Once(Form,Base):
    title = "Post One Article"
    subTitle = "Generate some motion"

    def update(self):
      context = self.context
      dateTimeNow = datetime.now()
      unixNow = dateTimeNow.timestamp()


      #Do Nothing in the middle of the night              
      if  0 < dateTimeNow.hour < 10:
          return          
                    
      if hasattr(context, 'webhooks'):
         for hook in context.webhooks.values():
             serverId = hook.serverId 
             articles  = context.hours24ApprovedArticles(unixNow,serverId)
             oldestArticle = articles [-1]
             if self.publishOrNot(unixNow,articles, serverId):
                  self.processOne(unixNow,oldestArticle, self.context)

    def publishOrNot(self,unixNow, articles,serverId):
        yesterday = unixNow - 24 *3600
        availableArticles = []
        publishedArticles = []
        for item in articles:
            if self.wasSent(item,serverId):
               publishedArticles.append(item)
            else:
               availableArticles.append(item)
            if len(publishedArticles) == 0:
                return True
            #Frequency in Hours   
            frequency = (24-10) / len(availableArticles)
            publishedAt = publishedArticles[-1].sentTo[serverId] 
            if (unixNow - publishedAt) > frequency :
                return True
        return False    

    def wasSent(self,article, to):
        if hasattr(article,'sentTo'):
           sentTo = article.sentTo 
           if to in sentTo:
               if sentTo[to] == True:
                  del sentTo[to]
                  return False
               return True
        return False

    def recordSending (self,unixTime,article,to):
        if not hasattr(article, 'sentTo'):
           article.sentTo = OOBTree()
           article.sentTo[to] = unixTime




