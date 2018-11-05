# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

from dolmen.template import TALTemplate

from os import path
TEMPLATE_DIR = path.join(path.dirname(__file__), 'templates')
def tal_template(name):
    return TALTemplate(path.join(TEMPLATE_DIR, name))









