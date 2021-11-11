# -*- coding: utf-8 -*-

import sys

from mastodon import Mastodon

from cromlech.browser import IURL
from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base.markers import FAILURE, SUCCESS
from dolmen.forms.base.utils import set_fields_data, apply_data_event
from dolmen.message.utils import send
from cromlech.browser.exceptions import HTTPFound

from zopache.core.getroot import getPrincipalFolder, getSiteRoot
from zopache.forms.validator import AccessGoogle
from zopache.pages.interfaces import IPage
from zopache.remote.mastodon.basebot import BaseBot
['write_media', 'write_statuses', 'read:accpimts']

class BaseAction(Action,BaseBot):
    def getData(self,form,codeName):
        self.form = form
        try:
           code = form.request.form[codeName]
           if len(code) == 0:
               raise Exception("Empty access token returned by Masotdon")
           breakpoint()
           mastodon= form.accountProxy(code)
           accountProxy = mastodon.log_in(code = code, redirect_uri= form.SITE,
                                          scopes= form.SCOPES)
                                   
           mastodonAccount = accountProxy.me()
           if not mastodonAccount['verified']:
                raise Exception ("Account not verified.")
           return  mastodonAccount, accountProxy, SUCCESS
        except Exception as error:
            msg = "while trying to process the access token there "
            msg +=  "was a problem. "
            msg += str(error)
            form.submissionError += msg
            return accountAccount,mastodonProxy, FAILURE
        
    def updateAccount(self,accountProxy,mastodonAccount,person):           
            longName = '@' + accountProxy.id + '@' + accountProxy.domain
            if longName not in person:
                new = Account()
                new.accountProxy = accountProxy
                mew.mastodonAccount = mastodonAccount
                new.id = accountProxy.id
                new.domain = accountProxy.domain
                new.userName = accountProxy.id
                person [longName]= new
                newURL = '/' + person.name 
                raise HTTPFound(newURL)
    
class CallBackAction(BaseAction):
    def __call__(self, form):
        self.form = form
        accountProxy, mastodonAccount, result = self.getData(form,'code')
        if result == FAILURE:
            return FAILURE
        people = form.getPrincipalFolder()
        email = mastodonAccount.email
        
        if email in people.idByEmail:
            personId = people.idByEmail[email]
            person = people [personId]
            people.loginUser(person)
            self.updateAccount(self,accountProxy,mastodonAccount,person)
            
        else:
            values = {}
            values["form-field-userName"] = accountProxy["username"] 
            values["form-field-userId"] = accountProxy["id"]            
            values["form-field-displayName"] = accountProxy["displayname"]
            values["form-field-domain"] = accountProxy["domain"]            
            values["form-field-email"] = accountProxy["email"]            
            values["code"] = accountProxy["code"]            
            values = form.urlEncode(values)
            url = '/mregister?' + values
            raise HTTPFound(url)

class RegisterAction(Action):            
    def __call__(self,form):
        self.form = form

        #First do the usual validation
        data, errors = self.form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE

        #Now the custom stuff.
        mastodonAccount, mastodonProxy, result = self. getData(
            form,'form-field-code')
        if result == FAILURE:
            return FAILURE
           
        new = form.factory()
        form.new=new
        new.email = mastodonAccount['email']
        new.title = mastodonAccount  ['displayName']
        siteRoot = form.getSiteRoot()
        people = form.getPrincipalfolder()
        newName = root.getUniqueNumberString()
        people[newName]=new
        new.name = newName
        #siteRoot.addItem(new)
        people.loginUser(new)   
        send("You are Registered")
        form.postAddProcess()
        self.updateAccount(self,accountProxy,mastodonAccount,person)


