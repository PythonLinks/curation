# -*- coding: utf-8 -*-

import deepl

from cromlech.browser import IURL
from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base.markers import FAILURE
from dolmen.forms.base.utils import set_fields_data, apply_data_event
from cromlech.browser.exceptions import HTTPFound
from ZODB.ExportImport import ExportImport
from zopache.core.uniquename import UniqueName
from cromlech.browser.interfaces import IPublicationRoot


class OneLanguage(Action):
    def __init__(self, title):
        super(Action, self).__init__(title)

    def __call__(self, form):
        self.form=form
        formData, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE

        targetLang = form.request.form['form.field.targetLanguage']
        if len(targetLang) !=2:
           form.submissionErrors = ["Please enter a 2 letter target language"]
           return
        if targetLang not in['de','fr','es','pl','tr','ja']:
           form.submissionErrors = ["Legal languages are de, fr,es,tk,pl,ja and tr."]
           return                  

        context = form.context
        allObjects =[]
        allStrings = []
        for item in self.form.context.allChildrenOfClass('Multilingual'):
            allObjects.append(item)
            allStrings.append(item.title)
            
        end = None #COULD BE 5 or NONE FOR WHOLE LIST
        
        with open('/app/data/deepl') as file:
            accessToken = file.readline()

        if end:
           allObjects = allObjects [:end]
           allStrings = allStrings [:end]
           
        translator = deepl.Translator(accessToken)

        tagetLang = targetLang.lower()
        result = translator.translate_text(allStrings,
                                   source_lang = 'en',
                                   target_lang=targetLang)
        
        form.status='Here are the translations:'
        if end == None:
           end  = len(allObjects) 
           
        for row in range(end):
           translatedText = result[row].text
           theObject = allObjects[row]
           theObject._p_changed = True           
           json = theObject.json

           if not targetLang in json:
               json[targetLang] = {}
           json[targetLang]['title']= translatedText
           
           form.status += "<br>"           
           form.status += "<br>"           
           form.status +=( str(row) + '. ' +
                           allStrings[row] + ' ' +
                           translatedText)



languages = ['de','es','fr','pl','tr','ja','nl']
    
class OneNode (Action):

    def __init__(self, title):
        super(Action, self).__init__(title)

    def __call__(self, form):
        self.form = form

        context = form.context
        englishTitle = context.title
        hasDescription = context.__class__.__name__ == 'Multilingual'
        if hasDescription:
            englishDescription = context.description

        englishContent = context.source
        
        json = context.json
        context._p_changed = True
        
        form.status='Here are the translations:'

        form.status += "en"
        form.status += "<br>"
        form.status += "Title"
        form.status += "<br>"        
        form.status +=  englishTitle
        form.status += "<br>"                        
        if hasDescription:
           form.status += englishDescription
           form.status += "<br>"
        form.status += "<br>"
        
        with open('/app/data/deepl') as file:
            accessToken = file.readline()

        translator = deepl.Translator(accessToken)
        
        for language in languages:
            if not language in json:
               json[language] = {}
            jsonLang = json[language]
            
            if englishTitle.strip():
               translatedTitle = translator.translate_text(
                                   englishTitle,
                                   source_lang = 'en',
                                   target_lang=language).text
            else:   
               transaltedTitle = ""               
            jsonLang['title'] = translatedTitle
            
            if hasDescription:
                if englishDescription.strip():
                    translatedDescription = translator.translate_text(
                                   englishDescription,
                                   source_lang = 'en',
                                   target_lang=language).text
                else:    
                   translatedDescription = ""
                jsonLang['description'] = translatedDescription
            
            if englishContent.strip():    
                translatedContent = translator.translate_text(
                                   englishContent,
                                   tag_handling = 'html',
                                   source_lang = 'en',
                                   target_lang=language).text            
            else:     
                translatedContent = ""
            jsonLang['content'] = translatedContent
            
            form.status += language + "<br> " 
            form.status +=  translatedTitle
            form.status += "<br>"
            if hasDescription:   
               form.status += translatedDescription
               form.status += "<br>"
            form.status += translatedContent
            form.status += "<br>"
            form.status += "<br>"            
           


        
        
