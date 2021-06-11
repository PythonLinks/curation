#uSED TO CREATE A SIMPLE INTERFACE TO SOCIAL DATA FOR JSON SCHEMA OBJECTS


class Social(object):
    def getTitle(self):
        return self.json[content][0]["title"]

    def getDescription(self):
        return self.content["english"]["description"]

    def getTwitterId(self):
        return self.getConnect("twitterId")
    
    def getFacebookURL(self):
        return self.getConnect("facebookURL")

    def getFacebookGroupURL(self):
        return self.getConnect("facebookGroupURL")
    
    def getFaceBookURL(self):
        return self.getConnect("facebookURL")
    
    def getInstagramURL(self):
        return self.getConnect("instagramURL")

    def getPhone(self):
        return self.getConnect("phone")

    def getEmail(self):
        return self.getConnect("email")        

    def getMastadonURL(self):
        return self.getConnect("mastadonURL")

    def youTubeURL(self):
        return self.getConnect("youTubeURL")    
    
    def getRemoteURL(self):
        return self.getConnect("remoteURL")

    remoteURL = property(getRemoteURL)
    twitterId = property(getTwitterId)        
    title = property(getTitle)
    description = property(getDescription)
    facebookURL = property(getFacebookURL)
    facebookGroupURL = property (getFacebookGroupURL)
    

        
    def getConnect(self,arg):
        return self.getJsonValue('connect',arg)
    
    def getJsonValue(self,arg1,arg2):
       if hasattr(self,'json'):
         if arg1 in self.json:
           item1 = self.json[arg1] 
           if arg2 in item1:
                 return item1 [arg2]
       return ""     
