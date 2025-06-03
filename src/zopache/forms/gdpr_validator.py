# -*- coding: utf-8 -*-
from dolmen.forms.base.errors import Error,Errors
from zopache.core.getroot import getPrincipalFolder
from zope.schema import ValidationError

class GDPRValidator(object):

    def __init__(self, fields, form):
        self.form = form

    def validate(self, data):
        self.data = data
        errors = Errors()
        chat = self.data['chatPermission']

        if not chat:
           msg = "GDPR Permission is required."
           identifier = "gdpr.permission.required"
           error = Error(msg,identifier)
           error.args = [msg]           
           errors.append(error)
        return errors
