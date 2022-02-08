import sys
from BTrees.OOBTree import OOBTree

from cromlech.security import permissions

from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.pages.interfaces import ICategory
from discord_webhook import DiscordWebhook, DiscordEmbed

@form_component
@context(ICategory)
@target(IView)
@name("webhooks")
@permissions('Manage')
class WebHook(Form):
    title = "Send By Webhook"
    subTitle = "For the newest approved articles publishes them."
             
    def update(self):
      context = self.context
      lastImportTime, values =  context.curatedHeadlines(count = 5)
      for article in values:
        for ancestor in article.ancestors():
          if hasattr(ancestor, 'webhooks'):
            self.processOne(article, ancestor)  

    def processOne(self,article,ancestor):
      for aHook in ancestor.webhooks.values():
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
           if 'Logo' in article:
               imageURL = self.secureShortURL(context = article) + "/Logo"
               embed.set_image(url=imageURL)
           try:
               response = webHook.execute()
           except :
              err = sys.exc_info()[0]
              self.status += str(err)
           self.recordSending(article, aHook.serverId)
           self.status += (" " + aHook.channelName + " " +
                         article.title + "<br>" )
           Form.update(self)

    def wasSent(self,article, to):
        if hasattr(article,'sentTo'):
           if to in article.sentTo:
               return True
        return False

    def recordSending (self,article,to):
        if not hasattr(article, 'sentTo'):
           article.sentTo = OOBTree()
           article.sentTo[to] = True
