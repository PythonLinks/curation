# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

import sys

from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.transport.requests import Request


from cromlech.browser import IURL
from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base.markers import FAILURE
from dolmen.forms.base.utils import set_fields_data, apply_data_event
from dolmen.message.utils import send
from cromlech.browser.exceptions import HTTPFound
from zopache.core.getroot import getPrincipalFolder, getSiteRoot

#import functools
#@functools.lru_cache(maxsize=40)
def validateToken(token,form,clientId):
        try:
          idinfo = id_token.verify_oauth2_token(token,Request(),clientId)
        except:
               raise ValueError('Trouble')            
        legit =['accounts.google.com', 'https://accounts.google.com']
        if  not (idinfo['iss'] in legit):
               raise ValueError('Wrong issuer.')
        return idinfo

def message(message):
    send(message)

class Cancel(Action):
    """Cancel the current form and return on the default content view.
    """

    def __call__(self, form):
        content = form.getContentData().getContent()
        url = str(IURL(content, form.request))
        return SuccessMarker('Aborted', True, url=url)

    
class GoogleLoginAction(Action):
    """Add action for an IAdding context.
    """
    def __init__(self, title, view):
        super(GoogleLoginAction, self).__init__(title)
        self.factory = view.factory
        self.view = view
        
    def getClientId(self,form):
        domain = form.getDomain()
        if (domain == 'pythonlinks.info'):
            clientId= '901181416018-8c8n8knds3b6koqkottchj7ivpncf409.apps.googleusercontent.com'
        elif (domain == 'dev.pythonlinks.info'):
            clientId = '901181416018-npba3s080378saoc1umjkn5jo7lipa1q.apps.googleusercontent.com'
        elif (domain == 'forestwiki.com'):
            clientId = '901181416018-8sh20u10e5tltf00jc4o8qfpq1jhmvh0.apps.googleusercontent.com'
        elif (domain == 'rights.men'):
            clientId = '901181416018-il4qps4qiqafom0uhmrppvcf9ao7ve07.apps.googleusercontent.com'
        elif (domain == 'golangvideos.com'):
            clientId = '901181416018-f6c7p85thdp79l9c6c3joccj9ffb5jug.apps.googleusercontent.com'
        elif (domain == 'stopsmog.info'):
            clientId = '901181416018-gmg5itiqs6f4cp5j5eot1corta0gd558.apps.googleusercontent.com'            
        else:
            raise ValueError('Bad Domain')
        return clientId
        
    def __call__(self, form):
        self.form = form
        try:
             data  = {'idtoken' :form.request.form['form.field.idtoken']} 
        except:
            data, errors = form.extractData()
            if errors:
               form.submissionError = errors
               return FAILURE
        token = data ['idtoken']
        try : 
            clientId = self.getClientId(form)
            if isinstance (token,list):
                token = token [0]

            self.data = data = validateToken(token,form,clientId)
        except ValueError:
            # Invalid token
            return "Invalide Token"
        people = getPrincipalFolder( form.context)
        userId = data['sub']
        self.innerCall(userId,people)
        
    def innerCall(self,userId,people):
        if userId in people:
            person = people[userId]    
            people.loginUser(person)   
            self.form.loggedIn = True

#SO BASICALLY IT NEEDS TO GO TO A LOGIN FORM
#IF THE USER EXISTS, LOG HIM IN AND REDIRECT.
#IF THE USER DOES NOT EXIST, SEND HIM TO THE
#REGISTER FORM.
#MY SCRIPT IS TOO COMPLEX
#WHAT MY SCRIPT DOES IS TRY TO LOG HIM IN
#ON SUCCESS REDIRECT TO PARENT
#ON FAILURE GO TO REGISTER PAGE
            
class GoogleRegisterAction(GoogleLoginAction):
    def innerCall(self,userId,people):
        if userId in people:
           raise Exception("THE USER ALREADY EXISTS")
        else:
           self.createUser(self.form, self.data, people)


    def createUser(self,form, data, people):
        obj=person= form.factory()
        form.new=obj
        newName = data ['sub']
        people[newName]=obj
        for key,value in data.items():
            if key in ['iss','sub','azp','aud','iat']:
               continue
            if key == 'name':
               obj.nameFromGoogle = data ['name']
               continue
            obj.__setattr__(key, value)
        root = getSiteRoot(form.context)
        root.addItem(obj)
        people.loginUser(person)   
        message("You are Registered")
        nextURL = ".."  
        raise HTTPFound(nextURL)

