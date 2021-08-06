

class Convert(object):

    def moveAttr(self,attrName,targetName, newName = None):
        newAttrName = newName or attrName
        if attrName in self.__dict__:
           attrValue = getattr(self,attrName)
           delattr(self,attrName)
           if attrValue != "":
               if not hasattr(self, targetName):
                   setattr(self,targetName,dict())
               getattr(self,targetName)[newAttrName] = attrValue

    def moveContent(self):
        self.content = dict()
        self.content["english"] = dict()
        
        self.content["english"]["description"] = self.description
        if "description" in self.__dict__:
           del self.__dict__["description"]
           
        self.content["english"]["source"] = self.source
        if "source" in self.__dict__:
            del self.__dict__["source"]
        
    def convert (self):
        #No Change to title and address.
        self.moveContent()
        self._p_changed = True

        self.candidateInfo = dict()
        self.candidateInfo["electionDate"] = "2020-11-03"

        if 'status' in self.__dict__:
           delattr(self,'status')
        self.candidateInfo = dict()
        self.candidateInfo["electionDate"] = "2020-11-03"
        self.moveAttr('twitterId','connect')
        self.moveAttr('phone','connect')
        self.moveAttr('instagramId','connect')
        self.moveAttr('remoteURL','connect')
        self.moveAttr('facebookId','connect', newName = "facebookURL")
        self.moveAttr('facebookGroup','connect',newName = "facebookGroupURL")
        self.moveAttr('youTubeChannelURL','connect')
        self.moveAttr('email','connect')

        self.moveAttr('eventsPageURL','candidateInfo')
        self.moveAttr('donationsPageURL','candidateInfo')
        self.moveAttr('hasScheduledEvents','candidateInfo')
        self.moveAttr('affiation','candidateInfo')
        self.moveAttr('districtURL','candidateInfo',newName = "districtMapURL")

        print (self.title)    
        if 'localOrNational' in self.__dict__:
            if len(self.localOrNational) >0:
                self.localOrNational= self.localOrNational.pop()
                self.moveAttr('localOrNational','candidateInfo')
            else:    
                delattr(self,'localOrNational')







        
