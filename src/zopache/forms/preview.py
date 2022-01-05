import json

from webpreview import web_preview
from cromlech.webob.response import Response
from dolmen.view import View

from zopache.ttw.JSON import makeJsonResponse
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import ISiteRootPage

@view_component

@name('fetchUrl')
@context(ISiteRootPage)
class Index(View):
    responseFactory = Response
    make_response = makeJsonResponse
        
    def render(self):
        try:
            url = self.request.form ['url']
            title, description, image = web_preview(url)
            result ={"success": 1,
                     "meta": {'title':title,
                              'url':url,
                      'description':description,
                      'image':{
                          'url':image}
            }}
            
            result = json.dumps(result)
            return result
        except:
            result = {
                "success" : 0,
                "meta": {
                }
            }
            result = json.dumps(result)
            return result
