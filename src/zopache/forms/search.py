from hypatia.catalog import CatalogQuery
import hypatia 
from hypatia.query import Contains
from more_itertools import take

def searchADictionary(view, aDict, defaultCategory = 'categories'):
    searchTerm = aDict.get("query","")
    type = aDict.get("type","video")
    recommended = aDict.get("recommended","recommended")
    category = aDict.get("category",defaultCategory)

    root = view.getSiteRoot()
    contentCatalog = root.contentCatalog
    q = CatalogQuery (contentCatalog)
    fields = [] 
    
    #NOW FOR RECOMMENDED
    if recommended == 'recommended':
        recommended = True
    elif recommended == 'other':
        recommended = False
        
        
    #NOW FOR THE TYPE 
    if type == "video":
       type = True
    elif type == 'article':
       type = False
     
   
    #FIRST FOR THE SEARCH TERM
    if searchTerm != "":
       fields.append(hypatia.query.Contains(contentCatalog['titlePlusDescription'], searchTerm))
    
    if recommended != "all":
        fields.append(hypatia.query.Eq(contentCatalog['recommended'], (recommended,recommended)))

    if type != 'both': 
           fields.append(hypatia.query.Eq(contentCatalog['isVideo'], (type,type)))

    if category != 'categories':
           fields.append(hypatia.query.Any(contentCatalog['ancestorNames'], [category]))

    #If NO SEARCH TERMS, RETURN ALL
    if len(fields) == 0:
        fields.append(hypatia.query.Eq(contentCatalog['isVideo'], (False,True)))

    myQuery = fields [0]
    for item in fields[1:]:
        myQuery = myQuery & item

    numdocs, docIds = q.query(
            myQuery,
            reverse=True,
            sort_index='importTime',
            limit=500
            )
    return numdocs, docIds

def valuesPlusRemainder(view,docIds):
    index = view.getSiteRoot().contentByTime
    values = [index[x] for x in take(6,docIds)]
    #NOTE DOCIDS IS NOW 6 SMALLER   
    return values, docIds

def justValues(view,docIds):
    index = view.getSiteRoot().contentByTime
    return  [index[x] for x in docIds]


