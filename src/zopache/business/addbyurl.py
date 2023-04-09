import json
import requests
from webpreview import web_preview

from dolmen.forms.base import Action, Actions, SuccessMarker
from dolmen.forms.base.errors import Error, Errors

from zopache.core.viewdecorators import *
from zopache.core.interfaces import ITreeSecurity
from zopache.crud.addbyurl import AddByURLForm
from zopache.crud.actions import Cancel
from zopache.crud.socialmedia import SocialMediaExtractor

#THE CLASSES TO ADD
from zopache.remote.rss import RSS
from zopache.business.company import Organization
from zopache.pages.page import Link
from zopache.pages.interfaces import IPage

class ProcessURL(object):
    def fetchURL(self,remoteURL,errors):
        try:
            response = requests.get(remoteURL)
            status = response.status_code
            if status != 200: 
                raise Exception ("Status Code " + str(status))
        except Exception as err:
            error = Error("Failed to Fetch URL" + str(err))
            errors.append(error)
            response = {}                        
        return [],response

        
@view_component
@name('addByURL')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddLinkByURL(AddByURLForm, ProcessURL):
    title = "Add a Link By URL"
    addSlug = "addLink"
    
    def processData(self,data):
        errors = Errors()
        remoteURL = data["remoteURL"]
        errors, response = self.fetchURL(remoteURL,errors)
        if errors:
           return errors, {}
        myDict = {}
        return  self.processPage(remoteURL,response,errors,myDict)

    
    def processPage(self,remoteURL, response,errors, myDict):
        try:
            title, description, image  = web_preview( remoteURL, content = response.content )
        except:
            error = Error("Web Preview Failed to Parse Response")
            return  errors.append(error) , response            
        
        myDict ['form.field.remoteURL'] = remoteURL
        if title:
           myDict ['form.field.title']= title
        if description:
            myDict['form.field.description']= description
        if image:
           myDict ['form.field.imageURL'] = image
        return  errors, myDict


class ProcessJSON(AddByURLForm,SocialMediaExtractor, ProcessURL):
    def processData(self,data):
        errors = Errors()
        remoteURL = data["remoteURL"]
        errors, response = self.fetchURL(remoteURL,errors)
        if errors:
           return errors, {}

        #NOW PROCESS THE PAGE RESPONSE
        myDict = self.getMyDict()
        errors,myDict = self.processPage(response,errors,remoteURL,myDict)
        if errors:
           return errors, {}
       
        connect = myDict["connect"]
        self.addSocialMedia(connect,response)
        response = json.dumps(myDict)
        return errors, {'json': response}

    def processPage(self,response,errors, remoteURL, myDict):
        try:
            title, description, image= web_preview(
                remoteURL, content = response.content )
        except Exception as err:
            error = Error("Failed to Preview Page" + str(err))
            errors.append(error)            
            return  errors,myDict
        self.saveData(remoteURL,title, description, image, myDict)
        return errors, myDict
    
@view_component
@name('addOrganizationByURL')
@target(IView)
@context(IPage)
class AddOrganizationByURL(ProcessJSON):
    allowAnonymous = True
    title = "Add an Organization By URL"
    addSlug = 'addOrganization'

    def getMyDict(self):
        return {"introduction": {},
                    "content":[{}],
                    "connect": {},
                    "organization":{}
        }
    
    def saveData(self,remoteURL, title,description,image,myDict):           

        myDict ['connect']['remoteURL'] = remoteURL
        myDict ['content'][0]['title']= title
        myDict['content'][0]['description']= description
        myDict ['introduction']['imageURL'] = image
        return myDict


@view_component
@name('addOnlineOrganizationByURL')
@target(IView)
@context(IPage)
class AddOnlineOrganizationByURL(AddOrganizationByURL):
    allowAnonymous = True
    title = "Add an Online Organization By URL"
    addSlug = 'addOnlineOrganization'


    
@view_component
@name('addCandidateByURL')
@target(IView)
@context(IPage)
class AddCandidateByURL(ProcessJSON ):
    allowAnonymous = True
    title = "Add a Candidate By URL "
    subTitle = "Just submit the URL for the candidate. "
    addSlug = 'addCandidate'        

    def getMyDict(self):
        return {"introduction": {}, 
                    "content":{"english":{}},
                    "connect": {},
                    "organization":{},
                    "candidateInfo":{}
        }
    
    def saveData(self,remoteURL, title,description,image,myDict):

        myDict ['connect']['remoteURL'] = remoteURL

        if title:
            myDict ['introduction']['title']= title
        
        if description:
            myDict['content']['english']['description']= description
            
        if image:
            myDict ['introduction']['logoURL'] = image
        return myDict
