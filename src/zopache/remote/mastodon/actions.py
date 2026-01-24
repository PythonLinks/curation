# What this does is first is first get the oauth code
# Then it creates a userLogin proxy
# Then it creates a user proxy
# Then it gets the user info.
# Then it logs the person in, or creates the account and logs them in. 
# Then redirects them to gdpr or to home.
# All a bit tricky.

# -*- coding: utf-8 -*-

import sys
import requests
from requests.models import urlencode
from urllib.parse import parse_qs

from mastodon import Mastodon

from cromlech.browser import IURL
from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base.markers import FAILURE, SUCCESS
from dolmen.forms.base.utils import set_fields_data, apply_data_event
from cromlech.browser.exceptions import HTTPFound

from zopache.core.getroot import getPrincipalFolder
from zopache.pages.interfaces import IPage
#from zopache.remote.mastodon.basebot import MastodonBot, GithubBot
from zopache.core.breadcrumbs import Breadcrumbs
from zopache.ttw.principalfolder import InternalPrincipal

class BaseAction(Action):
    def __call__(self, form):
        self.form = form
        view = form
        
        code, result = self.getOauthCode()
        if result == FAILURE:
            return FAILURE
        userLoginProxy , result = self.getUserLoginProxy(code)

        userInfo, result = self.getUserInfo(userLoginProxy)
                                        
        if result == FAILURE:
            return FAILURE
        
        principalFolder = view.getPrincipalFolder()
        userName = userInfo["username"]         
        email = userName + '@' + self.form.getOauthServer()
        handle = "@" + email
        if email in principalFolder.idByEmail:
            personId = principalFolder.idByEmail[email]
            person = principalFolder [personId]
            person.updateAccount(userLoginProxy,userInfo)
            principalFolder.loginUser(person,form)
            self.nextPage()
        else:
            person = principalFolder.newPerson(self.form)
            self.form.new = person
            person.email = email
            person.handle = handle
            if 'name' in userInfo:
                person.yourName = userInfo['name']
            person.updateAccount(userLoginProxy,userInfo)
            principalFolder [person.__name__] = person
            principalFolder.loginUser(person,form)            
            person.postAddProcess(view = form)
            self.goToGDPR()            

    def nextPage(self):
       principal = self.form.request.principal
       if ( principal.chatPermission and
            principal.postalCode):
            self.goHome()
       else:
            self.goToGDPR()
    
    def goToGDPR(self):
        form = self.form
        newURL = (form.getSecureLongURL (
                   context = form.getPrincipal())
                  + '/gdpr')        
        raise HTTPFound(newURL)

    def goHome(self):
        newURL = self.form.getSiteRoot().homePage
        raise HTTPFound(newURL)    
    
    def getOauthCode(self):
        code = self.form.request.form['code']
        try:
           if len(code) == 0:
               raise Exception("Empty access token returned by Masotdon")
        except Exception as error:
            msg = "while trying to get the access code "
            msg +=  "an empty access token was returned. "
            msg += str(error)
            self.form.submissionError += msg
            self.form.submissionErrors.append(msg)            
            return '', FAILURE
        return code, SUCCESS

class MastodonCallBackAction(BaseAction):
    def getUserLoginProxy(self,code):
        form = self.form
        try:
           mastodon = form.userLoginProxy(code)
           return mastodon, SUCCESS
        except Exception as error:
            msg = "while trying to get the access code "
            msg +=  "there was a problem. "
            msg += str(error)
            form.submissionError += msg
            form.submissionErrors.append(msg)
            return '', FAILURE

    def getUserInfo(self, userLoginProxy):
        form = self.form
        try:
            userInfo = userLoginProxy.me()
            return  userInfo, SUCCESS
        except Exception as error:
            msg = "while trying to get the User Info"
            msg +=  "was a problem. "
            msg += str(error)
            form.submissionError += msg
            print (msg)
            return {},FAILURE

class GithubCallBackAction(BaseAction):
        
    def getUserLoginProxy(self,code):
        url = "https://github.com/login/oauth/access_token"
        params = self.form.getParams()
        params['code'] = code
        response = requests.post(url,data=params)

        status = response.status_code
        if status == 200:
            parsedValue = parse_qs(response.text)
            if not 'access_token' in parsedValue:
               return {}, FAILURE

            return parsedValue, SUCCESS
        else:
            msg = "while trying to get the access code "
            msg +=  "there was a problem. "
            form = self.form
            form.submissionError += msg
            form.submissionErrors.append(msg)
            return {}, FAILURE

    def getUserInfo(self,userLoginProxy):
        # In the case of github, it is not really a long proxy.
        endPoint = "https://api.github.com/user"
        accessToken = userLoginProxy [ 'access_token'][0]
        if not accessToken:
            return {}, FAILURE
        
        headers = {'Authorization': 'token ' + accessToken}
        response = requests.get(endPoint, headers=headers)
        status = response.status_code
        if status == 200:
            result = response.json()
            result['username'] = result['login']
            return  result, SUCCESS
        else:
            msg = "while trying to get the user info "
            msg +=  "there was a problem. "
            form = self.form
            form.submissionError += msg
            form.submissionErrors.append(msg)
            return {}, FAILURE

