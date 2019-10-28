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
from zopache.core.getroot import getPrincipalFolder

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
            clientId = '461800128463-7s2kmmm3h7npkvu14lltv8dp1c58p3ie.apps.googleusercontent.com'
        elif (domain == 'climatevideos.info'):
            clientId = '982806744490-cvmnqkl4ovn9550sk56a1i6qjcean489.apps.googleusercontent.com'
        elif (domain == 'golangvideos.pl'):
            clientId = '333894959182-47b2vl06t1es006spak42gk7lvig490v.apps.googleusercontent.com'
        else:
            raise ValueError('Bad Domain')
        return clientId
    
    def validateToken(self,token,form):
        try:
          clientId = self.getClientId(form)
          # Specify the CLIENT_ID of the app that accesses the backend:
          idinfo = id_token.verify_oauth2_token(token,Request(),clientId)
        except:
               raise ValueError('Trouble')            

        legit =['accounts.google.com', 'https://accounts.google.com']
        if  not (idinfo['iss'] in legit):
               raise ValueError('Wrong issuer.')
        return idinfo

        
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
            self.data = data = self.validateToken(token,form)
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
            obj.__setattr__(key, value)
        people.loginUser(person)   
        message("You are Registered")

        try:
           obj.handle=data['given_name']+data['family_name']
        except:
           obj.handle = data['name']
        nextURL = form.nextURL()   
        raise HTTPFound(nextURL)

