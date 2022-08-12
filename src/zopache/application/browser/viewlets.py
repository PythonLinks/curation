# -*- coding: utf-8 -*-

from dolmen.viewlet import viewlet, Viewlet
from cromlech.browser import IURL, slot

from . import tal_template
from zopache.core.layout import ContextualActions

@viewlet
@slot(ContextualActions)
class Tabs(Viewlet):
    #tabs3.pt has the html for bootstrap 3 and ttw development
    #tabs4.pt has the html for bootstrap 4, file system wiki. 
    template = tal_template('tabs4.pt')
