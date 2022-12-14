
from zopache.remote.rssarticle import BaseArticle

class TootedArticle(BaseArticle):
    descruotion = ""
    def __init__(self,url,text,importTime, tootId):
        self.articleURL = url
        self.importTime = importTime
        self.source = text
        self.tootId = tootId

    def titlePlusDescription(self):
        return self.title + self.source

    async def processResponse(self, session, response,view):
        if 'image' in response.headers.get('content-type'):
           return await BaseArticle.processResponse(
              self,session, response,view)   
        else:
           return self.processTextResponse(
              session, response,view)       
       
    async def processTextResponse(self, session, response,view):        
        try:
            html  =  await response.text()
            title, description, image  = web_preview(
                         remoteURL, content = html )
        except:
            return  Error("Web Preview Failed to Parse Response")
         
        self.title = title

        self.source = description
          
        newName = slugify (self.title)
        newName = self.uniqueBothName (self,newName)
        print ("CREATING", newName)
        self.parent[newName] = self

        #LocalList
        self.localArticles[newName] = new
        new.postAddProcess(view )
