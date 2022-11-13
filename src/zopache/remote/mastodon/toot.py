from datetime import datetime, timedelta


from zope.interface import Interface
from zope.schema import Text, Float

from cromlech.browser.exceptions import HTTPFound
from dolmen.forms.base import Action,Actions
from dolmen.forms.base import Actions

from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm
from zopache.pages.interfaces import IPage
from zopache.remote.irss import IRSSArticle
from zopache.crud.update import Cancel, Edit
from zopache.crud.update import Edit
from zopache.remote.mastodon.basebot import BaseBot


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


class OnlyToot(Edit):
    def __call__(self, form):
        form.nowToot()
        
class OnlyTootAndView(Toot):
    def __call__(self, form):
        url = form.nowToot()
        if url != '':
           raise HTTPFound(url)
         
class Reset(Action):
    def __call__(self, form):
        form.context._toot = ""

class OnlyReset(Action):
    def __call__(self, form):
        raise HTTPFound(".")

class Delete(Action):
    def __call__(self, form):
        #Delete Image not supported.
        tootId = getattr(form.context,'tootId',None)
        if not tootId:
            form.submissionError += "No Toot to Delete"            
        try:
            result = form.getPrincipal().accountProxy.status_delete(tootId)
            del form.context.tootURL 
            del form.context.tootId 
        except Exception as error:
            form.report(error)
            form.submissionError += """
                 <br><br> Maybe that means that there is no such toot."""
            
    #2021 Looks like the Mastodon API does not support this
    """
    def deleteImage(self):
        
        image = self.parentalAcquire('Logo')
        mediaId = getattr(image,'mediaId',None)        
        if mediaId == None:
            form.submissionError += "No Image to Delete"
            return 
        try:
            result = form.proxyForUser().status_delete(tootId)
            del form.context.tootURL 
            del form.context.tootId 
        except Exception as error:
            form.report(error)
            form.submissionError += '''
                 <br><br> Maybe that means that there is no such toot.'''
         """  
        
class IClass(Interface):

    toot= Text(
        title = 'Toot',
        description = 'Say something!',
        required = False,
        default = '',
    )
    
    delay= Float(
        title = 'Delay',
        description = 'Hours until posted',
        required = False,
        default = 0.,
    )         

    
@form_component
@name ('toot')
@context(IPage)
class TootForm (EditForm,BaseBot):
    title = 'Toot'
    subTitle = 'Limit 500 characters'
    interface = IClass
    fields = Fields(IClass)
    tootURL = ""
    layoutName = "UserMenu"
    twitterId = ''
    link = ''
    accountProxy = False
    imageURL = ""
    scheduledAt = 0
    tempScheduledAt = 0
    
    def getTootImage(self):
        context = self.context
        banner = context.get('Banner',None)
        if banner != None:
            return banner
        
        logo = context.get('Logo',None)
        if logo != None:
            return logo

        return  self.parentalAcquire('Logo', context = context)
    
    def update(self):
        self.tootURL =  getattr(self.context,'tootURL','')
        self.tempTootURL =  getattr(self,'tootURL','')
        
        image = self.getTootImage()
        if image:
          self.imageURL = getattr(image, 'mastodonURL','')
 
        if hasattr(self.context,'rssFeed'): 
           rssFeed = self.context.rssFeed
           if hasattr(rssFeed,'twitterId'):
              self.twitterId = twitterId = rssFeed.twitterId
              self.link = ("https://twitter.com/" + twitterId) if twitterId else ''

        self.canToot =  getattr (self.request.principal,'accountProxy',False)
        
        self.template = self.getTemplates()['toot']
        self.updateLocalActions()
        EditForm.update(self)
    
    def nowToot(self):
         if self.context._toot == "":
            self.submissionError = """You submitted an empty toot, so nothing 
                               was posted. <br><br> The toot was reset to 
                              the defult toot."""
            return ''
        
         mediaList = self.mediaIdAsList()
         minDelay = 0.1 #(hours)
         try:
            delay = self.context.delay
            if delay < minDelay:
                delay = self.delay = 0
                scheduledAt = None
            else:    
                scheduledAt = datetime.now() + timedelta( hours=delay + 1 )
     
            tootDict = self.proxyForUser().status_post(self.context.toot,
                                            media_ids=mediaList,
                                            scheduled_at = scheduledAt
        )
                                 
            if self.isManager():
                target = self.context
            else:
                target = self
            #Only need to do this if
            #There is a future message
            if delay >= minDelay:
                at= tootDict["scheduled_at"]
                if at:
                   self.sendMessage("Your Toot will show up at: " +
                                 str(at))
                self.sendMessage("local Server Time: " +
                                 str(datetime.now()))                

            if tootDict.get('url',False):
                target.tootURL = tootDict.url
                   
            if tootDict.get('id',False):
                target.tootId = tootDict['id']

            if tootDict.get('schedule_at',False):
                target.scheduledAt = tootDict['scheduledAt']
                
            #Otherwise the delete action does not show up. 
            self.updateLocalActions()
            if 'url' in tootDict:                            
                return tootDict ["url"]
            return ""
        
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
        
    def updateLocalActions(self):
        if self.treeSecurity():
            self.addAuthorizedActions()
        else:
            self.addUnAuthorizedActions()
            
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

    def addUnAuthorizedActions(self):
        actionList = [OnlyToot("Toot","toot"),
                      OnlyTootAndView("Toot And View","tootView"),
                      OnlyReset("Reset",'reset')
                      ]
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
           mediaDict =   self.proxyForUser().media_post(media_file=data,
                                          mime_type=mimeType,
                                          description=self.context.title,
                                          focus=None)
           image.mastodonURL = mediaDict['url']
           image.mastodonId = mediaDict['id']           
           return [image.mastodonId]
        except Exception as error:
            self.report (error)
            return [] 


