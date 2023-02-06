from urllib.parse import urlparse
from slugify import slugify 
from zopache.business.addbyurl import ProcessURL
from zopache.crud.getimage import getImage
from zopache.remote.news.article import Article

class CreateArticle(ProcessURL):
    def processPage(self,remoteURL, response,errors, myDict):
        try:
            title, description, image  = web_preview( remoteURL, content = response.content )
        except:
            error = Error("Web Preview Failed to Parse Response")
            return  errors.append(error) , response            

        parsedURL = urlparse(url)
        hostname = parsedURL.hostName
        name = slugifyy (hostname)

        new = Article()
        new.name = name        
        new.remoteURL = remoteURL
        new.title = title
        new.description = description
        parent = self.siteRoot['newsServers']
        parent[name] = new
        getImage(new,image)
        
