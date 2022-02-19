from zopache.core.viewdecorators import *
from zopache.json.editjsonschema import AddJson, EditJson
from zopache.core.interfaces import ITreeSecurity
from zopache.business.company import Organization,OnlineOrganization
from zopache.business.interfaces import IOrganization, IOnlineOrganization
from zopache.pages.interfaces import IPage,IPageBase

class OnlineSchema(object):
    subTitle = ""
    schemaName = "OrganizationSchema"
    
    @property
    def jsonSchemaDict(self):
        result = getattr(self,'_jsonSchemaDict','')
        if result:
           return result 
        schema =  self.template[self.schemaName]
        result = schema.getAsDict()

        introduction = result ["properties"]["introduction"]
        introduction ["required"] = ["focus","logoURL"] 
        introduction = introduction ["properties"]
        del introduction["latitude"]
        del introduction["longitude"]
        del introduction["address"]        
        result = result
        self._jsonSchemaDict = result
        return result
    
@form_component
@name ('ckedit')
@context(IOrganization)
@implementer(ITreeSecurity)
class EditOrganization (EditJson):
    title = 'Edit this Multilingual Page.'
    subTitle = ''
    schemaName = "OrganizationSchema"

@form_component
@name ('ckedit')
@context(IOnlineOrganization)
@implementer(ITreeSecurity)
class EditOnlineOrganization (OnlineSchema,EditJson):
    title = 'Edit this Multilingual Page.'


@view_component
@name('addOrganization')
@target(IView)
@context(IPage)
class AddOrganization(AddJson):
    title = "Add an Organization"
    subTitle = ""
    factory = Organization
    schemaName = "OrganizationSchema"

    def newName(self,data):
        newName =  self.requestJsonDict["content"][0]['title']
        return newName
        
    def dataModel(self):
        return "{}"
        #contextJsonDict =  self.template['newOrganizationJson'].getAsDict()
        #result = json.dumps(contextJsonDict)
        #return result
    
@view_component
@name('addOnlineOrganization')
@target(IView)
@context(IPageBase)
class AddOnlineOrganization (OnlineSchema,AddOrganization):
    title = "Add an Online Organization"
    subTitle = ""
    factory = OnlineOrganization

