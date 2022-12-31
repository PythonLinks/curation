import sys
import time

from slugify import slugify

from zope.interface import implementer

from dolmen.forms.base.markers import FAILURE, SUCCESS
from dolmen.container import OrderedBTreeContainer

from zopache.remote.rssarticle import BaseArticle
from zopache.remote.mastodon.interfaces import ITootedArticle
from zopache.remote.rssdownload import fetch
from zopache.crud.getimage import createImageInFrom
from webpreview import web_preview

@implementer(ITootedArticle)
class TootedArticle(BaseArticle):
    webClass = "TootedArticle"
    webApproved = True
    publicationApproved = True
    descruotion = ""
    title = ""

    def __init__(self,url,content,importTime,tootId,tootURL):
        self.articleURL = url
        self.importTime = importTime
        self.description = content
        self.tootId = tootId
        self.tootURL = tootURL
        self.content = content
        self.count = 0
        #Simpler to not call page initialization.
        #Base Article sets import time. Not good. 
        #HOPE I DO NOT MISS ANYTHING
        OrderedBTreeContainer.__init__(self)
        self.modificationTime= time.time()
        
    
    def titlePlusDescription(self):
        return self.title + self.source

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

        self.title = title
        self.imageURL = image
        self.source = description
        newName = slugify (self.title)
        newName = view.uniqueBothName (self,newName)
        parent = self.parent
        parent[newName] = self
        parent.localArticles[newName] = self
        self.postAddProcess(view )
        if image:
           return await fetch(session,self,view)
        else:
           return SUCCESS, self 
