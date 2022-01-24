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


#THIS ONE IS THE WORKHORSE
# FOR FANCYTREE AND DESKTOP VIEW
@view_component
@name('json')
@title("JSON")
@target(IView)
@context(ICategory)
class MYJSON(View):
    responseFactory = Response
    make_response = make_json_response
    def render(self):
        # USED TO HAVE TIGHER SECURITY       
        #if self.context.__name__ in
        #   ['cloud-native','python','climate-change']:
        #return 'JSON is not available for that object.'
        return "NOT YET IMPLEMENTED"

       

#THIS ONE JUST GETS THE TREE OF CATEGORIES

@view_component
@name('categories.json')
@target(IView)
@context(ICategory)
class JSONCategories(View):
    responseFactory = Response
    make_response = make_json_response
    def render(self):
            return json.dumps(self.context.asDict(), indent = 2)

@view_component
@name('allCategories')
@target(IView)
@context(ICategory)
class AllCategories(View):
    responseFactory = Response
    make_response = make_json_response
    def render(self):
            return self.context.allChildrenOfClass('Category')
        



 
