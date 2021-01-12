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
from zopache.forms.validator import AccessGoogle
from zopache.pages.interfaces import IPage

class Cancel(Action):
    """Cancel the current form and return on the default content view.
    """

    def __call__(self, form):
        content = form.getContentData().getContent()
        url = str(IURL(content, form.request))
        return SuccessMarker('Aborted', True, url=url)


class GoogleLoginAction(Action,AccessGoogle):
    """Add action for an IAdding context.
    """
    def __init__(self, title, view):
        super(GoogleLoginAction, self).__init__(title)
        self.factory = view.factory
        self.view = view
        
        
    def __call__(self, form):

        self.form = form
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE
        token = data ['idtoken']
        del data ['idtoken']
        self.data = data
                
        self.getTokenData(token)
        people = getPrincipalFolder(form.context)

        email = self.tokenData['email']

        self.innerCall(email,people)
        
    def innerCall(self,email,people):
        if email in people.idByEmail:
            personId = people.idByEmail[email]
            person = people [personId]

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
    def innerCall(self,email,people):
        if email in people.idByEmail:
           raise Exception("THE USER ALREADY EXISTS")
        else:
           self.createUser(self.form, people)


    def createUser(self,form, people):
        self.form = form
        obj=person= form.factory()
        form.new=obj
        newName = self.tokenData ['sub']
        people[newName]=obj

        for key,value in self.tokenData.items():
            if key in ['iss','sub','azp','aud','iat']:
               continue
            if key == 'name':
               obj.nameFromGoogle = value
               continue
            obj.__setattr__(key, value)
            
        for key,value in self.data.items():
            obj.__setattr__(key, value)                
        root = getSiteRoot(form.context)
        root.addItem(obj)
        people.loginUser(person)   
        send("You are Registered")
        form.postAddProcess()
        newURL = self.form.newURL() 
        raise HTTPFound(newURL)

    
