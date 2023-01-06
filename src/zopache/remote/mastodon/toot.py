import sys
import time

from slugify import slugify

from webpreview import web_preview

from bs4 import BeautifulSoup

from zope.interface import implementer

from cromlech.container.contained import Contained
from dolmen.forms.base.markers import FAILURE, SUCCESS
from dolmen.container import BTreeContainer

from zopache.remote.rssarticle import BaseArticle
from zopache.remote.mastodon.interfaces import ITootedArticle
from zopache.remote.rssdownload import fetch
from zopache.crud.getimage import createImageInFrom
from zopache.pages.used import Used
from zopache.remote.sharedarticle import SharedArticle
from zopache.core.ancestors import Ancestors
from zopache.ttw.html import UntrustedHTMLBase
from cromlech.container.contained import Contained
from zopache.core import Container

@implementer(ITootedArticle)
class TootedArticle(Container,
                    SharedArticle,
                    Used,
                    UntrustedHTMLBase):
    
    webClass = "TootedArticle"
    webApproved = True
    publicationApproved = True
    description = ""
    title = ""
    content = ""
    recommended = True
    
    def __init__(self,url,content,importTime,tootId,tootURL):
        SharedArticle.__init__(self)        
        self.articleURL = url
        self.importTime = importTime
        self.description = content or "" 
        self.tootId = tootId
        self.tootURL = tootURL
        self.content = content
        self.count = 0
        #Simpler to not call page initialization.
        #Base Article sets import time. Not good. 
        #HOPE I DO NOT MISS ANYTHING



    @property
    def publishedAt(self):
        return self.importTime
    
    def preDeleteProcess(self,view):
        localArticles = self.curator.localArticles
        try:
           del localArticles [self.tootId]
        except:
           raise Exception("""Could not delete that tootedarticle
           from local articles.""", tootId)
       
    @property
    def titlePlusDescription(self):
        #This can be deleted. 
        if self.description == None:
            self.description = ""
        if self.title == None:
            self.title = ""            
        return self.title + self.description

    def tagsAsHTML(self):
        return self.tags
    
    async def processResponse(self, session, response,view):
        contentType = response.headers.get('content-type').lower()

        if 'text'in contentType:
           return await self.processTextResponse(
              session, response,view)
        elif 'image' in contentType:
           result =  await self.processImageResponse(session, response,view)
              
           return result
        else:
          return (FAILURE, 'Bad contentType in tooted article' +
                  contentType)

    async def processImageResponse(self,session, response, view):
        try:
            content =  await response.content.read()
            contentType = response.headers['content-type']
            createImageInFrom(self,content, contentType, 'Logo')
            print ("*", end = "")            
            return SUCCESS, self
        except:
            e = sys.exc_info()[0]
            return FAILURE, node.__name__ + str(e)     

    async def processTextResponse(self, session, response,view):        
        try:
            html  =  await response.text()
            title, description, image  = web_preview(self.articleURL, content = html )
                         
        except:
            return  FAILURE, "Web Preview Failed to Parse Response"
        if not title:
            return FAILURE, "NO TITLE GIVEN"
        self.title = title
        self.imageURL = image
        self.source = description
        newName = slugify (self.title)
        newName = view.uniqueBothName (self,newName)
        curator= self.curator
        parent = self.parent
        parent[newName] = self
        print (".",end = "")
        curator.localArticles[self.tootId] = self
        self.postAddProcess(view )
        if image:
           return await fetch(session,self,view)
        else:
           return SUCCESS, self
       
    def defaultToot(self,view):
        toot = self
        soup = BeautifulSoup(toot.description, 'html.parser')
        result = ""
        for tag in soup.contents:
            result += tag.text
            if tag.name == 'p':
                result += "\n"
        return   (
                result +
                "\n\n" +
                toot.curator.mastodonId +
                "'s #BestToots\n\n" +
                self.articleURL +
               "\n\n" +
               "More:"  + 
               "\n\n" +
                toot.tags + " "
                )
