
class NewsMixIn(object):
    #To make a simple unified codebase
    #All of the inheritors get a default toot array
    #Just make sure that the first time you
    #Add somethign to it, to create a new array
    toots = []
    
    def getVia(self):
        result = ""
        for toot in self.toots:
            result += toot.parent.userName() + ' '
        return result
    
    def getDescription(self,view):
        for item in self.toots:            
            if len(item.articles) == 1:
                if item.content:
                    return item.content
        return self.description

    def getBoosts(self):
        boosts = 0
        for item in self.toots:
            boosts += item.numberOfBoosts
        return boosts
    
    def addToot(self,toot):
        #Because, to save space,  some have a shared class toot list.
        if len (self.toots) == 0:
           self.toots = [] 
        self.toots.append(toot)
        self.p_changed = True

    def hasToots(self):
        return len (self.toots) > 0

    def removeToot(self,toot):
        self.toots.remove(toot)
        self.p_changed = True

    def removeAllToots(self):
        if len(self.toots)==0:                    
           return
        
        for aToot in self.toots:
            aToot.removeArticle(self)        
        self.toots =[]
        self.removeFromShortList()
