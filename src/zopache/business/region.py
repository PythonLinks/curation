from zopache.core.relatives import Parents
from zopache.business.interfaces import IPoliticianCollection
from zopache.business.politician import IPolitician

class Region(Parents):

    def getPolitians (self):
        parents = self.parentsWhichImplement(IPoliticianCollection)
        parents.reverse
        byClass = map(lambda x: x.sortByClass(), parents)   
        politiicans = byClass[0]['Politician']
        parentLength = len(parents)

        #THE NATIONAL PAGE
        if parentLength == 1;
            children = (byClass[0]['Organization'] +
                        byClass[0]['MapOrganization'])
            for item in children:
                all = item.getCompaniesRecurisvely()
                for item  in all:
                  if ((IPolitician.providedBy(item)) and 
                    (item.localOrNational == 'National')):
                      politicians append (item)
            return politicians
        
        #THE STATE PAGES
        elif parentLength == 2:
            children = parents[1].getCompaniesRecursively()
            for item in children:
                if IPoliticina.providedby(item):
                   politicians.append(item)
            return policians
        
        #FOR LOCAL PAGES 
        if parentLength > 2:
            politicinas = []
            for item in parents:
                if IPolitician.providedBy(item):            
                   politicians.append(item)
        return politians    
