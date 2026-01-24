# -*- coding: utf-8 -*-
from dolmen.forms.base.errors import Error,Errors
from zopache.core.getroot import getPrincipalFolder
from zope.schema import ValidationError
from z3c.schema.email import isValidMailAddress

class GDPRValidator(object):

    def __init__(self, fields, form):
        self.form = form

    def validate(self, data):
        self.data = data
        errors = Errors()
        mastodonId = self.data['mastodonId']
        emailAddress = self.data['emailAddress']
        if len(mastodonId) !=0:
           if ((mastodonId[0] != '@') or
               not isValidMailAddress(mastodonId[1:])):
                   msg = "Not a valid Mastodon or Discord Id."
                   identifier = "not.valid.id"
                   error = Error(msg,identifier)
                   error.args = [msg]           
                   errors.append(error)

        if len(emailAddress) !=0:
           if  not isValidMailAddress(emailAddress):
                   msg = "Not a valid email address."
                   identifier = "not.valid.email"
                   error = Error(msg,identifier)
                   error.args = [msg]           
                   errors.append(error)                               
        
        if not mastodonId and not emailAddress:
           msg = """Either a Mastodon or Discord id or Email Address is needed to contact you."""
           identifier = "contact.info.required"
           error = Error(msg,identifier)
           error.args = [msg]           
           errors.append(error)
        return errors
