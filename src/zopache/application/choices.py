from slugify import slugify
from zope.schema.vocabulary import SimpleVocabulary

def fromList(aList,includeNone=False):
    terms = []
    if includeNone == True:
        term = SimpleVocabulary.createTerm('None','None','None')
        terms.append(term)
        
    for item in aList:
        token = slugify (item)
        term = SimpleVocabulary.createTerm(token,item,item)
        terms.append(term)
    return SimpleVocabulary(terms)

def fromDict(choiceDict,includeNone=False):
    terms = []
    if includeNone:
        term = SimpleVocabulary.createTerm('None','None','None')
        terms.append(term)

    for key,value in choiceDict.items():
        term = SimpleVocabulary.createTerm(key,key,value)
        terms.append(term)
    return SimpleVocabulary(terms)
