# -*- coding: utf-8 -*-


import sys


from cromlech.browser import IURL
from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base.markers import FAILURE
from dolmen.forms.base.utils import set_fields_data, apply_data_event
from dolmen.message.utils import send
from cromlech.browser.exceptions import HTTPFound

from zopache.core.getroot import getPrincipalFolder, getSiteRoot
from zopache.forms.validator import AccessGoogle
from zopache.pages.interfaces import IPage
from zopache.remote.mastodon.basebot import BaseBot



            

