from hypatia.catalog import CatalogQuery
import hypatia 
from hypatia.query import Contains
from more_itertools import take

def searchADictionary(view, aDict, defaultCategory = None):
    if defaultCategory == None:
        defaultCategory = view.context.name
    searchTerm = aDict.get("query","")
    type = aDict.get("type","both")
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
        
    originalType = type    
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
            limit = 1000,
            sort_index='importTime'
            )
    if searchTerm:
       return numdocs, [], docIds
   
    category = root[category]

    #Fixing a naming difference
    if originalType == 'article':
       originalType = 'articles'
    if originalType == 'video':
       originalType = 'videos'
       
    try:
        content = category.json[originalType]
    except:
        return numdocs, [], docIds
   
    if len(content) == 0:
       return numdocs, [], docIds            

    featuredTimes= set()
    featuredItems = []
    for row  in content:
           name = row['name'].strip()
           if not name in root:
              continue 

           item = root[name]
           featuredItems.append(item)
           time = item.importTime
           featuredTimes.add (time)
    notFeaturedIds = []
    for time in docIds:
        if time not in featuredTimes:
           notFeaturedIds.append(time)
           
    #returning list(featuredTimes) incorrectly sorts them by importTime.
    featuredTimes =  [item.importTime for item in featuredItems]           
    return numdocs, featuredTimes,  notFeaturedIds
        
def valuesPlusRemainder(view,docIds, count = 6):
    index = view.getSiteRoot().contentByTime
    values = [index[x] for x in take(count,docIds)]
    
    #NOTE DOCIDS IS NOW 6 SMALLER   
    return values, docIds

def justValues(view,docIds):
    index = view.getSiteRoot().contentByTime
    return  [index[x] for x in docIds]


