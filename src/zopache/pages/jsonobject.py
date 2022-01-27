import json
from dolmen.container import IBTreeContainer

from dolmen.view import View
#from dolmen.view import name, context, view_component
from cromlech.webob.response import Response

from zopache.core.viewdecorators import *
from zopache.pages.interfaces import ICategory


def make_json_response(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or u'')
        response.content_type=u'application/json'
        return response    

#GETS ALL THE ARTICLES
@view_component
@name('json')
@target(IView)
@context(ICategory)
class MYJSON(View):
    responseFactory = Response
    make_response = make_json_response
    def render(self):
        if self.context.__name__ not in ['categories']:
           return 'JSON is not available for that object.'
        asDict = self.context.asDict(classes =['Category','RSS','RSSArticle'])
        return json.dumps(asDict, indent = 2)
                                     

#THIS ONE JUST GETS THE TREE OF CATEGORIES

@view_component
@name('categories.json')
@target(IView)
@context(ICategory)
class JSONCategories(View):
    responseFactory = Response
    make_response = make_json_response
    def render(self):
        if self.context.__name__ not in ['categories']:
           return 'JSON is not available for that object.'
        asDict =  self.context.asDict()
        return json.dumps(asDict,  indent = 2)               

@view_component
@name('allCategories')
@target(IView)
@context(ICategory)
class AllCategories(View):
    responseFactory = Response
    make_response = make_json_response
    def render(self):
            return self.context.allChildrenOfClass('Category')
        



 
