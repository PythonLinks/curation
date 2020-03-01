# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.
from PIL import Image as PilImage
from cromlech.browser import IURL
from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base.markers import FAILURE
from dolmen.forms.base.utils import set_fields_data, apply_data_event
from zopache.crud import i18n as _
from dolmen.message.utils import send
from cromlech.browser.exceptions import HTTPFound
from zope.event import notify
from zope.location import ILocation
from zope.lifecycleevent import ObjectCreatedEvent
from zopache.ttw.html import HTML
from zopache.ttw.javascript import Javascript
from zopache.ttw.css import CSS
from zopache.ttw.JSON import JSON
from zopache.ttw  import File, Image
from ZODB.blob import Blob

def message(message):
    send(message)

class AddFileAction(Action):
    """Add action for files.
    """
    
    def __init__(self, title):
        self.title = title
        super(AddFileAction, self).__init__(title)

    def __call__(self, form):
        self.form=form
        formData, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE
        self.upload(formData)
        self.message()
        nextURL = self.nextURL()
        #self.new.postAddProcess(view=form)
        return SuccessMarker('Added', True, url=nextURL ,code=307)

    def nextURL(self):
        baseURL = self.form.url(self.form.context)
        return baseURL + "/manage"

    def message(self):    
        message(u"File Uplaoded")        

    def upload(self, formData):
        file = self.createFile(formData)
        name=formData['__name__']
        context = self.form.context
        newName=self.form.uniqueContainerName(context,name)        
        context[newName] = file
        self.new = file
        return file
        
    def createFile(self,formData):
        nextView= '/'
        fileUpload =  formData ['data']
        contentType = fileUpload.headers.get_content_type()
        fileName = fileUpload.filename        
        if True:
            data = fileUpload.file.read()
            
            if contentType=='txt/html':
               file=HTML()
               file.source=data
               nextView +=  fileName+'/ckedit'

            elif contentType=='txt/css':
               file=CSS()
               file.source=data
               nextView +=  fileName+'/aceedit'
               
            elif (contentType.lower() in
                   ['txt/json',
                    'application/json']): 
               file=JSON()
               file.__name__ = fileName
               file.source=data
               nextView  += fileName+'/aceedit'               

            else:
               file = File()
               file.__name__ = fileName
               file.data = data
               nextView = '/manage'
            file.contentType = contentType
            self.nextView=nextView
            return file

class AddImageAction(AddFileAction):
    def message(self):    
        message(u"Image Uploaded")


    def createFile(self,formData):
         self.nextView = '/manage'
         file = Image()
         imageData  = formData['data']
         imageData.file.seek(0)         
         file.data = imageData #Inside it reads the file.read()
         imageData.file.seek(0)
         image = PilImage.open(imageData.file, mode = 'r')
         file.contentType = imageData.type
         file.width = image.width
         file.height = image.height
         file.title = formData ["title"]   
         return file

        
