from mastodon import Mastodon

from zope.interface import Interface
from zope.schema import Text

from cromlech.browser.exceptions import HTTPFound
from dolmen.forms.base import Actions

from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm
from zopache.remote.irss import IRSSArticle
from zopache.crud import update as editactions

class IClass(Interface):

    toot= Text(
        title = 'Toot',
        description = 'Say something!',
        required = False,
        default = '',
    )         

@form_component
@name ('toot')
@context(IRSSArticle)
@permissions('Manage')
class Toot (EditForm):
    title = 'Toot'
    subTitle = 'Limit 500 characters'
    interface = IClass
    fields = Fields(IClass)
    tootURL = ""
    
    def postToot2(self):
         if self.context._toot == "":
            self.submissionError = """You submitted an empty toot, nothing 
                               was posted.  <br>Here is the default toot for this 
article. """
            return
         mastodon = Mastodon(
          access_token = self.getPrincipal().accessToken,
          api_base_url = 'https://mastodon.social')
         
         try:
            tootDict = mastodon.status_post(self.context.toot,
                                     visibility = "direct")
            tootURL = self.tootURL = tootDict.url
         except Exception as error:
            self.submissionError += str(error)
            return
         raise HTTPFound(tootDict.url)

    def update(self):
        #Ideally should do the next line, but it does nothing extra.
        #EditForm.update(self)
        self.template = self.getTemplates()['toot']    
        if self.treeSecurity():
            self.addAuthorizedActions()
    
    def addAuthorizedActions(self):
        self.actions = Actions(editactions.Edit("Toot","toot"),
                    editactions.Cancel("Cancel","Cancel"))
        
    def acquireTitle(self):
        return 'Toot about: ' + self.context.title 

    def postProcess(self,view = None):
        self.postToot2()
        
    def mediaIdAsList(self):
        image = self.parentalAcqure('Logo')
        mediadict = getattr(image,'mediadict',None)
        if mediaDct != None:
           return [mediaDict['id']] 
        data , mimeType = image.mastadonImage()
        try: 
           mediaDict =   Mastodon.media_post(data,
                                          mime_type=mimeType,
                                          description=self.context.ttle,
                                          focus=None)
           image.mastadonURL = mediaDict['url']
           image.mastadonId = mediaDict['id']           
           return [image.mastadonId]
        except Exception as e:
            print(e)
            return [] 

    def postToot(self):
        status = self.toot
        try:
            tootDict = Mastodon.status_post(status,
                             media_ids=self.mediaIdsAsList(),
                             language="eng")
        except Exception as e:
             print(e)
        self.context.tootURL = tootDict['url']
        self.context.tootId = tootDict['id']        
