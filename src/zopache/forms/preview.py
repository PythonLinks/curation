import json
import requests
import base64
from zope.interface import Interface

from webpreview import web_preview
from cromlech.webob.response import Response
from dolmen.view import View
from cromlech.browser.interfaces import IPublicationRoot

from zopache.ttw.JSON import makeJsonResponse
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import ISiteRootPage
from zopache.core.breadcrumbs import Breadcrumbs

@view_component
@name('fetchUrl')
@context(Interface)
class Index(View,Breadcrumbs):
    responseFactory = Response
    make_response = makeJsonResponse
        
    def render(self):
        try:
            url = self.request.form ['url']
            if self.getDomain() in url.lower():
                return self.localPreview(url)
            else:
                return self.remotePreview(url)

        except:
            result = {
                "success" : 0,
                "meta": {
                }
            }
            result = json.dumps(result)
            return result

    def notUsedPreview(self):
            result ={"success": 1,
                     "meta": {'title':title,
                              'url':url,
                      'description':description,
                      'image':{
                          'url':image}
            }}
            
    def remotePreview(self,url):
        #title, description, image = web_preview(url)
        title = """ERROR: Only Curated (Local) Links can be added"""
        description = "The problem has to do with caching the images, "
        description += "as accessing images across domains " 
        description += "is genrally not allowed."
        image = None
        result ={"success": 1,
                     "meta": {'title':title,
                              'url':url,
                      'description':description,
                      'image':{
                          'url':image}
            }}
        try:
            if image != None:
                response  = requests.get(image)
                image = result['meta']['image']
                if response.status_code == 200:
                    mime = response.headers['Content-Type']
                    data = response.content
                    data = base64.b64encode(data).decode('utf-8')
                    image['mime-type'] = mime
                    image['image-data'] = data 
        except:
            pass
        result = json.dumps(result)
        return result
        
    def localPreview(self,url):
         parts = url.split('/')
         slug = parts[-1].strip()
         if slug == "article":
             slug = parts [-2].strip()

         siteRoot = self.getSiteRoot()
         item = siteRoot[slug]
         parent = item.parent
         logo = self.parentalAcquire('Logo')
         time  = int(getattr(item,'publishedAt','') or item.creationTime)
         remoteURL  = (getattr(item,'articleURL','')
                       or getattr(item,'remoteURL','') or
                       url)
         try:
             twitterId = item.rssFeed.twitterId
         except:
             twitterId = ""
         imageURL = ("https://" + self.getDomain() + '/' +
                      slug + "/Logo150W"
         )

         result ={"success": 1,
                     "meta": {'title':item.title,
                              'url':url,
                              'slug':slug,
                              'time': time, 
                              'description':item.description,
                              'parentSlug' : parent.name,
                              'parentTitle': parent.title,
                              'remoteURL': remoteURL,
                              'twitterId': twitterId,
                              'image':{
                                  'url': imageURL,
                                  'attributionText': logo.attributionText,
                                  'attributionURL': logo.attributionURL
                                  }
                              }
                }
            
         result = json.dumps(result)
         return result
