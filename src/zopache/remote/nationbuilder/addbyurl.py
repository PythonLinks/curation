
from base64 import b64encode

from bs4 import BeautifulSoup

from dolmen.forms.base.errors import Error, Errors

from zopache.core.viewdecorators import *
from zopache.business.addbyurl import ProcessJSON
from zopache.pages.interfaces import IPageBase

from .interfaces import IFetchData
from webpreview import web_preview
@view_component
@name('moveData')
@target(IView)
@context(IPageBase)
class MoveData(ProcessJSON ):
    interface = IFetchData
    addSlug = "addNBPage"
    def processData(self,data):
        errors = Errors()
        #FIRST GET THE PAGE
        remoteURL = data["remoteURL"]
        errors, response = self.fetchURL(remoteURL,errors)
        if errors:
           return errors, {}

        #NOW PROCESS THE PAGE RESPONSE
        myDict = self.getMyDict()
        errors, myDict= self.processPage(response,errors,myDict,remoteURL)
        if errors:
           return errors, {}
       
        #NOW GET THE IMAGE
        imageURL = data["imageURL"]
        if imageURL != "":
            errors, response = self.fetchURL(remoteURL,errors)
            if errors:
               return errors, {}       

        errors,myDict = self.processImage(response,errors,myDict)
        if errors:
           return errors, {}
       
        return errors,{'json': myDict}
   
    def getMyDict(self):
        return {"introduction": {}}


    def processPage(self,response,errors,myDict,remoteURL):
        try:
            title, description, image  = web_preview( remoteURL, content = response.content )
            myDict['introduction']['title'] = title
            myDict['introduction']['description'] = description
        except:
            error = Error("Web Preview Failed to Parse Response")
            return response, errors.append(error)            
        
        try: 
           soup = BeautifulSoup(response.content, 'html.parser')
           content =  soup.find(class_="content")
           myDict['introduction']['source'] = str(content)
        except Exception as err:
            error = Error("Failed to Parse Page" + str(err))
            errors.append(error)            
        return errors, myDict
        
    def processImage(self,response,errors,myDict):
        if response.status_code != 200:
            error = Error("Web Preview Failed to Fetch Image")
            return errors.append(error), {}            
        
        myDict ['introduction']['image'] =  (
            b64encode(response.content).decode('utf-8'))
        
        return errors, myDict
