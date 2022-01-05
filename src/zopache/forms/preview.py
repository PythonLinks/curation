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

    def remotePreview(self,url):
            title, description, image = web_preview(url)
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
         siteRoot = self.getSiteRoot()
         slug = url.split('/')[-1]
         item = siteRoot[slug]
         parent = item.parent
         
         result ={"success": 1,
                     "meta": {'title':item.title,
                              'url':url,
                              'description':item.description,
                              'parentSlug' : parent.name,
                              'parentTitle': parent.title,       
                              'image':{
                                  'url':url + '/Logo150W'}
                              
            }}
            
         result = json.dumps(result)
         return result
