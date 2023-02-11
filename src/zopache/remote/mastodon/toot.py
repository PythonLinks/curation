import sys
import time
import re

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
                     "www.twitter.com",
                     "climatejustice.social",
                     "c.im"}


@implementer(IToot)
class Toot(Leaf):
    webClass = "Toot"
    webApproved = False
    publicationApproved = False
    description = ""
    content = ""
    source = ""
    recommended = False
    numberOfBoosts = 0
    numberOfFavorites = 0
    count = 0
    
    def __init__(self):
        Leaf.__init__(self)
        self.articles = []
        self.articleURLs = []

    @property    
    def title(self):

        if self.articles:
            return self.articles[0].title
        return self.content[0:30]
    
    def addArticle(self,article):
        self.articles.append(article)
        url = (getattr(article, 'articleURL', False) or
                   article.remoteURL)        
        self.articleURLs.remove (url)                       
        self._p_changed = True        
        
    def removeArticle(self,article):
        self.articles.remove(article)
        url = (getattr(article, 'articleURL', False) or
                   article.remoteURL)        
        self.articleURLs.append(url)
        self._p_changed = True
        
    def createToot(self,toot,account):
        if toot.reblog:
            return None
        self.source =  toot.content
        soup = BeautifulSoup(toot.content, 'html.parser')
        text = soup.get_text()
        if not soup.text.strip():
            return None
           
        try:
            language = detect(text)
        except LangDetectException as e:
            return None
        if language != 'en':
            return None 

        soup, textTags = self.removeHashTags(soup)
        soup, articleURLs = self.processURLs (soup)
        self.articleURLs = articleURLs
        if len(articleURLs) == 0:
            return None
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
        self.description = ""
        self.tootId = tootId
        self.tootURL = toot.url
        return self

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
        for article in self.articles.copy():
            self.removeArticle(article)
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
                   text = tag.text
                   textTags.append(text)
                   result= re.findall('[A-Z]*[^A-Z]*', text[1:])
                   result.remove('')
                   #print ("SPLIT= ", result)
                   text = ' '.join(result)
                   tag.replace_with(text)
                                             
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

   
