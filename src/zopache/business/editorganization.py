from zopache.core.viewdecorators import *
from zopache.business.editjsonschema import AddJson, EditJson
from zopache.core.interfaces import ITreeSecurity
from zopache.business.company import Organization,OnlineOrganization
from zopache.business.interfaces import IOrganization, IOnlineOrganization

@form_component
@name ('ckedit')
@context(IOrganization)
@implementer(ITreeSecurity)
class EditOrganization (EditJson):
    title = 'Edit this Multilingual Page.'
    subTitle = ''
    schemaName = "OrganizationSchema"  


from zopache.pages.interfaces import IPageBase
@view_component
@name('addOrganization')
@target(IView)
@context(IPageBase)
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
    
