import sys
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

from slugify import slugify

from webpreview import web_preview

from bs4 import BeautifulSoup

from zope.interface import implementer

from dolmen.forms.base.markers import FAILURE, SUCCESS
from zopache.remote.mastodon.interfaces import IToot

from zopache.core import Leaf

hostNamesToIgnore = {"uncensorednews.us",
                     "takvera.blogspot.com",
                     "twitter.com",
                     "www.twitter.com"}


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

    def createToot(self,toot,account):
        if toot.reblog:
            return None, []
        self.source = content = toot.content
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()
        if not soup.text.strip():
            return None , []
           
        try:
            language = detect(text)
        except LangDetectException as e:
            return None , []
        if language != 'en':
            return None , []

        soup, textTags = self.removeHashTags(soup)
        soup, articleURLs = self.processURLs (soup)
        if len(articleURLs) != 1:
            return None,articleURLs
        url = articleURLs[0]
        soup.smooth()
        soup = self.removeEmptyParagraphs(soup)
            
        #NOW CREATE THE TOOT   
        self.content = str(soup)
        self.tags = ' '.join(textTags)
        self.parent =  account
        tootId = str(toot.id)
        self.name = tootId
        self.hasMedia =  True if toot.media_attachments else False
        self.userId = toot.account.acct
        self.numberOfBoosts = toot.reblogs_count
        self.numberOfFavorites = toot.favourites_count

        self.articleURL = url
        self.description = ""
        self.tootId = tootId
        self.tootURL = toot.url
        return self, articleURLs

    def processURLs(self,soup):    
        urls  = soup.find_all('a')
        articleURLs = []
        for item in urls:
            #Ignore Mentions     
            text = item.get_text() 
            if not text:
                continue
            if text and text[0]=='@':
               continue
           
            url = item["href"]
            item.replace_with('')            
            if not url:
                continue
            hostName = urlparse(url).hostname
            if not hostName:
               continue                
            if hostName.lower() in hostNamesToIgnore:
               continue
            articleURLs.append(url)
            
        return soup, articleURLs
    
    def preDeleteProcess(self,view):
        article = getattr(self,'article',None)
        if article:
            article.removeToot(self)
    
    def tagsAsHTML(self):
        return self.tags
    
    def updateValue(self,name,newValue):
        if getattr(self,name,None) != newValue:
            setattr(self,name,newValue)
            
    #Iterate through destroying all but the last hash tag. 
    def removeHashTags(self,soup):
        hashTags =  []
        textTags = []                        
        
        previousTag = None
        lastWasHashTag = False
        contents = soup.contents
        for paragraph in contents:
            for tag in paragraph:
                #skip spaces
                if not tag.text.strip():
                    continue
                if self.isHashTag(tag):
                    if not lastWasHashTag:
                        hashTags.append([])
                    hashTags [-1].append(tag)
                    lastWasHashTag = True
                else:
                    lastWasHashTag = False 

        for sequence in hashTags:

            if len (sequence) > 1:
               for tag in sequence:
                       textTags.append(tag.text)
                       tag.replace_with('')
            else:
               for tag in sequence:
                   textTags.append(tag.text)                   
                   tag.replace_with(tag.text)
        return soup,textTags
        
    def isHashTag(self,tag):
       try:
           if tag.name == 'a':
              if tag.text[0] == '#':
                  return True
       except:
           pass
       return False    

    def removeEmptyParagraphs(self,soup):
        for item in soup:
            if not item.text.strip():
               item.replace_with('')
        return soup       

   
