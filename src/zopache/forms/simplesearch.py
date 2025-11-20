from hypatia.catalog import CatalogQuery
import hypatia 
from hypatia.query import Contains
from itertools import islice
from more_itertools import take

def getResults(view, aDict, limit=10):
    root = view.getSiteRoot()
    searchTerm = aDict.get("q","")
    contentCatalog = root.contentCatalog
    q = CatalogQuery (contentCatalog)
    fields = list()
    searchTerm = aDict.get("q","")    
    if searchTerm != "":    
       fields.append(hypatia.query.Contains(
               contentCatalog['titlePlusDescription'],
               searchTerm))
    else:
        return (0,[])
    myQuery = fields[0]        
    numDocs, docIds = q.query(
            myQuery,
            limit = limit
#           ,sort_index='importTime'
            )
    return numDocs, docIds

