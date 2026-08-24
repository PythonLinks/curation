# -*- coding: utf-8 -*-
from dolmen.forms.base.errors import Error,Errors
from zope.schema import ValidationError

class PostalValidator(object):

    def __init__(self, fields, form):
        self.form = form

    def validate(self, data):
        self.data = data
        errors = Errors()
        postalCode = self.data['postalCode']

        if postalCode:
           length = len(postalCode) 
           if ((length not in [0,5]) or
               (not str.isdigit(postalCode))):
               msg = "Your zip code must be exacly 0 or 5 digits"
               identifier = "Postal.Code.Error"
               error = Error(msg,identifier)
               error.args = [msg]           
               errors.append(error)
        return errors
