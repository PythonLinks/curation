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
    
    def __init__(self, title,factory):
        super(AddFileAction, self).__init__(title)

    def __call__(self, form):
        self.form=form
        formData, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE

        self.upload(formData)
        self.message()
        baseURL = self.form.url(self.form.context)
        url = baseURL + self.nextView
        self.new.postAddProcess()
        return SuccessMarker('Added', True, url=url,code=307)

    def saveFile(self,file,formData):
        name=formData['__name__']
        context = self.form.context
        newName=self.form.uniqueName(context,name)        
        self.form.context[newName] = file
        file.__parent__=self.form.context
        file.__name__=newName

    def saveDetails(self,file,fileUpload):    
        file.contentType=fileUpload.type
        file.title = fileUpload.filename
        
    def message(self):    
        message(u"File Uplaoded")        

    def upload(self, formData):
        file = self.createFile(formData) 
        self.saveFile(file,formData)
        self.new = file
        return file
        
    def createFile(self,formData):
        nextView ='/'
        fileUpload =  formData ['data']
        contentType = formData ['data'].headers.get_content_type()
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

            self.saveDetails(file,fileUpload)
            self.nextView=nextView
            return file

class AddImageAction(AddFileAction):
    def message(self):    
        message(u"Image Uploaded")


    def createFile(self,formData):
         nextView ='/'
         fileUpload =  formData ['data']
         contentType = formData ['data'].headers.get_content_type()
         fileName = fileUpload.filename        

         data = fileUpload.file.read()
         file = Image()
         file.__name__ = fileName
         file.data = data
         nextView = '/manage'

         self.saveDetails(file,fileUpload)
         self.nextView=nextView

         image = PilImage.open(fileUpload.file, mode = 'r')
         self.width = image.width
         self.height = image.height
         
         return file

        
