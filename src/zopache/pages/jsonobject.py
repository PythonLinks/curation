#JSON VIEWS ON OBJECTS
from zopache.pages.interfaces import IPage,IRootPage
from zopache.core.viewdecorators import *
import datetime
from dolmen.container import IBTreeContainer
from zope.interface.interface import Attribute
from dolmen.view import View
from dolmen.view import name, context, view_component
from cromlech.browser.directives import title
from crom import target, order
from cromlech.container.interfaces import IOrderedContainer
from zopache.business.interfaces import ICompany

from zopache.categories.treewidget import IConference, IConferenceContainer
try:
    pass
except:
    pass

class JsonObject(object):
    
    #FUNCTION TO GET JSON TREE OF CATEGORIES
    #JUST CATEGORIES, NO DATA
    def categoryVariables(self,spacing):
         result=''
         result+=',\n'
         result+=spacing


         #PROVIDE THE TEXT LINE
         name='title'
         text='\"'+name+'\": \"'
         text += self.title 
         text+='\"'

         #PROVIDE THE WebCLASS
         text+= ',\n   '
         name='class'
         text += '\"'+name+'\": \"'
         webClass = self.webClass
         if webClass in ["GoogleMap","HomePage"]:
             webClass = "Category"
         text += webClass
         text += '\"' 
         
         return text

     
    #FUNCTION TO GET VARIABLE FOR A PAGE TREE
    def treeVariables(self,spacing):
         theURL='/'+self.__name__
         result=''
         result+=',\n'
         result+=spacing


         #PROVIDE THE TITLE
         name='title'
         text='\"'+name+'\": \"'
         text += self.title 

         text+='\"' 

         #AND NOW THE DATA
         data= ',\n\"data\":{'

         #PROVIDE THE SHORT URL
         data+= '\n   '
         name='shortURL'
         data += '\"'+name+'\": \"'
         data += theURL 
         data += '\"' 

         #PROVIDE THE CREATION TIME
         data+= ',\n   '
         name='creationTime'
         data += '\"'+name+'\": \"'
         data += str(self.creationTime)
         data += '\"' 

         #PROVIDE THE TITLE
         data+= ',\n   '
         name='title'
         data += '\"'+name+'\": \"'
         data += self.title
         data += '\"' 

         #PROVIDE THE webCLASS
         data+= ',\n   '
         name='class'
         data += '\"'+name+'\": \"'
         data += self.webClass
         data += '\"'

         #PROVIDE THE URL
         if (hasattr(self,'url') and (self.url != "")):
             data+= ',\n   '
             name='url'
             data += '\"'+name+'\": \"'
             data += self.url
             data += '\"'          

         #PROVIDE THE DESCRIPTION
         data+= ',\n   '
         name='description'
         data += '\"'+name+'\": \"'

         data += self.description
         data += '\"' 

         #PROVIDE THE BRANCH SIZE
         data+= ',\n   '
         name='branchSize'
         data += '\"'+name+'\": \"'
         data += str(self.branchSize)
         data += '\"'


         if hasattr(self,'conference') and (self.conference != None):
              data+= ',\n   '
              name='conference'
              data += '\"'+name+'\": \"'
              try:
                 data += self.conference.__name__
              except:
                 data +="pycon-us-2018" 
              data += '\"'


         # END THE DATA SECTION
         data+='}'         
         

         return text+data

    def jsonTree(self,indent):
        return '[' +  self.getJSON(indent,'treeVariables') + ']'

    def jsonCategories(self,indent):
        return '[' +  self.getJSONCategories(indent,'categoryVariables') + ']'    


#AND HERE FOR JUST THE CATEOGIRES
    def getJSONCategories(self,indent,aFunction):
        result=''
        spacing=' '*indent*2
        shortSpacing = ' '*(2*indent-1)
        result += '\n'+shortSpacing
        result += '{'
        result+= '\"key\": \"'+ getattr(self,'__name__')+'\"'
        result+=',\n'
        
        #NOW GET THE VARIBLgES
        result+=getattr(self,aFunction)(spacing)

        #NOW GET THE CONTAINED OBJECTS
        valuesLength=len(list(self.values()))

        if valuesLength> 0:
                  result+=',\n \"folder\":true'
                  result+=',\n'
                  result += spacing + '\"children\":'
                  result += '['

        if IOrderedContainer.providedBy(self):
            firstLine=True
            for item in self.values():
                if ((item.__class__.__name__ == 'Conference') or
                    (item.__class__.__name__ == 'ConferenceContainer' )):

                   if not firstLine:
                      result+=',' 
                   else:
                      firstLine=False
                   result+=item.getJSONCategories(indent+1,aFunction)
        if valuesLength> 0:
             result+=']'
        result+='}'
        return result

    
#AND HERE YOU HAVE THE GENERIC ONE
    def getJSON(self,indent,aFunction):
        result=''
        spacing=' '*indent*2
        shortSpacing = ' '*(2*indent-1)
        result += '\n'+shortSpacing
        result += '{'
        result+= '\"key\": \"'+ getattr(self,'__name__')+'\"'
        result+=',\n'
        
        #NOW GET THE VARIBLgES
        result+=getattr(self,aFunction)(spacing)

        #NOW GET THE CONTAINED OBJECTS
        valuesLength=len(list(self.values()))

        if (IPage.providedBy(self)):
             if (valuesLength> 0):
                 result+=',\n \"folder\":true'

        if valuesLength> 0:
                  result+=',\n'
                  result += spacing + '\"children\":'
                  result += '['

        if IOrderedContainer.providedBy(self):
            firstLine=True
            for item in self.values():
                if (IPage.providedBy(item) and
                   (not ICompany.providedBy(item)) and
                   item.webApproved):
                   if not firstLine:
                      result+=',' 
                   else:
                      firstLine=False
                   result+=item.getJSON(indent+1,aFunction)
        if valuesLength> 0:
             result+=']'
        result+='}'
        return result



from crom import target, order
from cromlech.browser.directives import title
from cromlech.security import permissions
from dolmen.view import name, context, view_component
from dolmen.view import View
from cromlech.webob.response import Response

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
@context(IPage)
class MYJSON(View):
    responseFactory = Response
    make_response = make_json_response
    def render(self):
        # USED TO HAVE TIGHER SECURITY       
        #if self.context.__name__ in
        #   ['cloud-native','python','climate-change']:
        #return 'JSON is not available for that object.'
        return self.context.jsonTree(2)

       

#THIS ONE JUST GETS THE TREE OF CATEGORIES

@view_component
@name('categories.json')
@title("JSON")
@target(IView)
@context(IPage)
class JSONCategories(View):
    responseFactory = Response
    make_response = make_json_response
    def render(self):
            return self.context.jsonCategories(2)



 
