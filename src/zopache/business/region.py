from zopache.core.relatives import Parents
from zopache.business.ipolitician import IPolitician
from zopache.business.interfaces import IOrganization
from zopache.business.ipolitician import IPolitician

class Region(object):
    def parentsWhichImplement(self,interface):
           item = self
           result=[]
           while (item!=None):
             if interface.providedBy(item):
                       result.append(item)
             item=item.__parent__
           return result

    def getPoliticians (self):
        parents = self.parentsWhichImplement(IOrganization)
        parents.reverse()
        parentLength = len(parents)
        
        #THE NATIONAL PAGE
        if parentLength == 1:
            siteRoot = self.getSiteRoot()
            nationalPoliticians = siteRoot.nationalPoliticians.values()
            return nationalPoliticians

        #FOR STATE AND LOCAL MAPS FIRST GET THE TWO NATIONAL
        #POLITICIANS IN THE NATIONAL MAP.  HOWIE AND ANGELA
        byClass = list(map(lambda x: x.sortByClass(), parents))
        politicians = byClass[0]['Politician']
        #THE STATE PAGES
        if parentLength == 2:
            children = []
            children = self.getCompaniesRecursively(children)
            for item in children:
                if IPolitician.providedBy(item):
                   politicians.append(item)
            return politicians
        
        #FOR LOCAL PAGES 
        if parentLength > 2:
            politicians = []
            for parent in parents:
                for item in parent.values():
                    print (parent.__name__, item.__name__)
                    if IPolitician.providedBy(item):
                        print (item.__name__)
                        politicians.append(item)
            return politicians    
