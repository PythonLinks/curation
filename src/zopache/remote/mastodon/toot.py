import sys
import time

from slugify import slugify

from webpreview import web_preview

from bs4 import BeautifulSoup

from zope.interface import implementer

from dolmen.forms.base.markers import FAILURE, SUCCESS
from zopache.remote.mastodon.interfaces import IToot

from zopache.core import Leaf

@implementer(IToot)
class Toot(Leaf):
    webClass = "Toot"
    webApproved = False
    publicationApproved = False
    description = ""
    title = ""
    content = ""
    source = ""
    recommended = False
    numberOfBoosts = 0
    numberOfFavorites = 0
    count = 0
    def __init__(self,url,content,tootId,tootURL):
        Leaf.__init__(self)
        self.articleURL = url
        self.description = ""
        self.source = content or "" 
        self.tootId = tootId
        self.tootURL = tootURL

    def tagsAsHTML(self):
        return self.tags
    
