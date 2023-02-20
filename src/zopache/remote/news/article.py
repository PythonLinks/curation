from slugify import slugify
from inspect import currentframe, getframeinfo

from webpreview import web_preview
from dolmen.forms.base.markers import FAILURE, SUCCESS

from zopache.pages.page import Link
from zopache.remote.rssdownload import fetch
from zopache.crud.getimage import createImageInFrom

class Article (Link):
    webClass = "RSSLink"
    toots = None
    importTime = 0
    description = ''
    title = ''
    __name__ = ''

    
    def __init__(self, toot, url, account, mastodonArticles):
        Link.__init__(self)
        self.toots = []
        if 'red' in toot.tags:
            self.red = True
        if 'yellow' in toot.tags:
            self.yellow = True

        self.articleURL = url
        hostName = urlparse(url).hostname
        domainName = account.domainName
        if domainName and (domainName in hostName):
           self.webApproved = False
        self.parent = root.get(
           account.defaultCategory,
           self.mastodonArticles)
    
    def titlePlusDescription(self):
        return (self.title + ' ' +
                self.description)
        
    def preDeleteProcess(self,view):
        for toot in self.toots:
            toot.removeArticle(self)
            self.toots = []
    
    async def processResponse(self, session, response,view):
        #if 'aus.social' in self.articleURL: 
        #    break point()
        #if 'c.im' in self.articleURL: 
        #    break point()            


        try:
            contentType = response.headers.get('content-type').lower()
        except:
           return FAILURE, self, "ContentType was not defined." 

        if 'text'in contentType:
           return await self.processTextResponse(
              session, response,view)
        elif 'image' in contentType:
           result =   await self.processImageResponse(session,
                                                      response,
                                                      view)
           return result
        else:
          frameinfo = getframeinfo(currentframe())
          return (FAILURE,
                  (frameinfo.filename + ' ' +
                  str(frameinfo.lineno) + ' ' +
                  contentType),
                  self)

    async def processImageResponse(self,session, response, view):
        try:
            content =  await response.content.read()
            contentType = response.headers['content-type']
            createImageInFrom(self,content, contentType, 'Logo')
            return SUCCESS, self
        except:
          frameinfo = getframeinfo(currentframe())
          e = sys.exc_info()[0]          
          return (FAILURE,
                  (frameinfo.filename + ' ' +
                   str(frameinfo.lineno) + ' ' +
                   str(e)),
                   self)
                              
    async def processTextResponse(self, session, response,view):
        try:
            html  =  await response.text()
            title, description, image  = web_preview(self.articleURL, content = html )
        except:
            return  FAILURE, "Web Preview Failed to Parse Response"

        if description == None:
            description = ""
        #This is a link to a Mastodon server, quit
        if (
           "To use the Mastodon web application, please enable JavaScript."
           in html):
             return  FAILURE, "This is a mastodon server"
        if not title:
            return FAILURE, "NO TITLE GIVEN", self
        self.title = title
        self.imageURL = image
        if view.siteRoot.existsRemoteURL(self.articleURL):        
           return
       
        if len(description) > 100:
           decription = description[100:]
           description = description.rsplit(' ', 1)[0]
           description = description + "..."
        self.description = description
        newName = slugify (self.title)
        newName = view.uniqueBothName (self,newName)
        parent = self.parent
        parent[newName] = self
        print (".",end = "")
        self.postAddProcess(view )
        if image:
           return await fetch(session,self,view)
        else:
           return SUCCESS, self.name + "but no image"
       
    def postAddProcess(self,view):
        pass
    
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
