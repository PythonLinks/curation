from zopache.core.viewdecorators import *
from zopache.json.editjsonschema import AddJson, EditJson
from zopache.core.interfaces import ITreeSecurity
from zopache.business.company import Organization,OnlineOrganization
from zopache.business.interfaces import IOrganization, IOnlineOrganization
from zopache.pages.interfaces import IPage,IPageBase
from zopache.business.jsonschemavalidator import JSONSchemaValidator
from zopache.business.exists import DuplicateOrganization
from zopache.forms.urlvalidator import DuplicateURLValidator
from zopache.business.exists import Duplicate

@form_component
@name ('ckedit')
@context(IOrganization)
@implementer(ITreeSecurity)
class EditOrganization (EditJson):
    title = 'Edit this Multilingual Page.'
    subTitle = ''
    schemaName = "OrganizationSchema"


@view_component
@name('addOrganization')
@target(IView)
@context(IPageBase)
class AddOrganization(AddJson):
    title = "Add an Organization"
    subTitle = ""
    factory = Organization
    schemaName = "OrganizationSchema"
    dataValidators = [JSONSchemaValidator,
                      DuplicateOrganization,
                      DuplicateURLValidator]
    
    def newName(self,data):
        newName =  self.requestJsonDict["content"][0]['title']
        newName = self.uniqueBothName(self.context, newName)
        return newName
        
    def dataModel(self):
        return "{}"
        #contextJsonDict =  self.template['newOrganizationJson'].getAsDict()
        #result = json.dumps(contextJsonDict)
        #return result

from zopache.json.jsonmaporganization import JSONMapOrganization

@view_component
@name('addJSONMapOrganization')
@target(IView)
@context(IPageBase)
class AddJSONMapOrganization(AddOrganization):
    title = "Add a JSON Map Organization"
    subTitle = ""
    factory = JSONMapOrganization
    schemaName = "OrganizationSchema"
    
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
@context(IOnlineOrganization)
@implementer(ITreeSecurity)
class EditOnlineOrganization (OnlineSchema,EditJson):
    title = 'Edit this Multilingual Page.'


    
@view_component
@name('addOnlineOrganization')
@target(IView)
@context(IPageBase)
class AddOnlineOrganization (OnlineSchema,AddOrganization):
    title = "Add an Online Organization"
    subTitle = ""
    factory = OnlineOrganization

