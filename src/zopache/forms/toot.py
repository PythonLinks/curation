from mastodon import Mastodon

from zope.interface import Interface
from zope.schema import Text

from cromlech.browser.exceptions import HTTPFound
from dolmen.forms.base import Action,Actions
from dolmen.forms.base import Actions

from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm
from zopache.remote.irss import IRSSArticle
from zopache.crud.update import Cancel, Edit
from zopache.crud.update import Edit



class Toot(Edit):
    def __call__(self, form):
        Edit.__call__(self,form)
        form.nowToot()
        
class TootAndView(Toot):
    def __call__(self, form):
        Edit.__call__(self,form)
        form.nowToot()
        if getattr(form.context, 'tootURL',None):
             raise HTTPFound(form.context.tootURL)

class Reset(Action):
    def __call__(self, form):
        form.context._toot = ""

class Delete(Action):
    def __call__(self, form):
        #Delete Image not supported.
        #self.deleteImage(form)
        self.deleteToot(form)
        
    def deleteToot(self,form):
        tootId = getattr(form.context,'tootId',None)
        if not tootId:
            form.submissionError += "No Toot to Delete"            
        try:
            result = form.mastodon.status_delete(tootId)
            del form.context.tootURL 
            del form.context.tootId 
        except Exception as error:
            form.report(error)
            form.submissionError += """
                 <br><br> Maybe that means that there is no such toot."""
            
    #2021 Looks like the Mastodon API does not support this
    def deleteImage(self):
        
        image = self.parentalAcquire('Logo')
        mediaId = getattr(image,'mediaId',None)        
        if mediaId == None:
            form.submissionError += "No Image to Delete"
            return 
        try:
            result = form.mastodon.status_delete(tootId)
            del form.context.tootURL 
            del form.context.tootId 
        except Exception as error:
            form.report(error)
            form.submissionError += """
                 <br><br> Maybe that means that there is no such toot."""            
        
class IClass(Interface):

    toot= Text(
        title = 'Toot',
        description = 'Say something!',
        required = False,
        default = '',
    )         

class Remote(object):
    @property
    def mastodon(self):
        return  Mastodon(
          access_token = self.getPrincipal().accessToken,
          api_base_url = 'https://mastodon.social')

    
@form_component
@name ('toot')
@context(IRSSArticle)
@permissions('Manage')
class TootForm (EditForm,Remote):
    title = 'Toot'
    subTitle = 'Limit 500 characters'
    interface = IClass
    fields = Fields(IClass)
    tootURL = ""
    layoutName = "UserMenu"

    
    def nowToot(self):
         if self.context._toot == "":
            self.submissionError = """You submitted an empty toot, so nothing 
                               was posted. <br><br> The toot was reset to 
                              the defult toot."""
            return False
        
         mediaList = self.mediaIdAsList()

         try:
            tootDict = self.mastodon.status_post(self.context.toot,
                                                 media_ids=mediaList)
            self.context.tootURL = tootDict.url
            self.context.tootId = tootDict['id']
            
            #Otherwise the delete action does not show up. 
            if self.treeSecurity():
               self.addAuthorizedActions()            
            return True
         except Exception as error:
            self.report(error)
            self.submissionError += """ <br><br> 
               Sorry about that. 
               Try reducing the number of charactrs by 5. 
               <br><br>"""
            return False
        
    def report (self,error):
        self.submissionError += (error.args[3] if len(error.args) > 3
                                        else str(error))
        
    def update(self):
        #Ideally should do the next line, but it does nothing extra.
        #EditForm.update(self)
        self.template = self.getTemplates()['toot']
        if self.treeSecurity():
            self.addAuthorizedActions()
    
    def addAuthorizedActions(self):
        actionList = [Edit("Save",'save'),
                      Toot("Toot","toot"),
                            TootAndView("Toot And View","tootView"),
                            Reset("Reset",'reset')
                            ]
        if hasattr(self.context,'tootURL'):
              actionList.append(Delete("Delete Toot","deleteToot"))
        actionList.append(Cancel("Cancel","Cancel"))
        actionList = tuple(actionList)                  
        self.actions = Actions(*actionList)

        
    def acquireTitle(self):
        return 'Toot about: '
    
    @property
    def subTitle(self):
       return  self.context.title 

    def postrocess(self):
        pass
    
    
    def mediaIdAsList(self):
        image = self.parentalAcquire('Logo')
        mediaId = getattr(image,'mediaId',None)
        if mediaId != None:
           return [mediaId]
        data , mimeType = image.mastodonImage()
        
        try: 
           mediaDict =   self.mastodon.media_post(media_file=data,
                                          mime_type=mimeType,
                                          description=self.context.title,
                                          focus=None)
           image.mastodonURL = mediaDict['url']
           image.mastodonId = mediaDict['id']           
           return [image.mastodonId]
        except Exception as error:
            self.report (error)
            return [] 


