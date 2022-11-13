#uSED TO CREATE A SIMPLE INTERFACE TO SOCIAL DATA FOR JSON SCHEMA OBJECTS

#FIRST the Basics TITLE, DESCRIPTION, SOURCE
class BasicProperties(object):
    
    def getTitle(self):
           return self.json['content'][0]["title"]

    def setTitle(self,value):
        self.json['content'][0]["title"] = value
        
    title = property(getTitle,setTitle)    

    def getDescription(self):
        return self.json['content'][0].get("description","")

    def setDescription(self,value):
        self.json['content'][0]["description"] = value

    description = property(getDescription, setDescription)
        
    @property    
    def source(self):
        return self.json['content'][0].get("source","")

    def getIntroduction(self,arg):
        return self.getJsonValue('introduction',arg)    

    def getJsonValue(self,arg1,arg2):
       if hasattr(self,'json'):
         if arg1 in self.json:
           item1 = self.json[arg1] 
           if arg2 in item1:
                 return item1 [arg2]
       return ""     

#NOW THE SOCIAL MEDIA LINKS   
class SocialProperties(BasicProperties):
    def getTwitterId(self):
        return self.getConnect("twitterId")

    def setTwitterId(self,id):
        self.json["connect"]["twitterId"] = id    
    twitterId = property (getTwitterId,setTwitterId)
    
    @property
    def facebookPage(self):
        return self.getConnect("facebookPage")

    @property
    def facebookGroup(self):
        return self.getConnect("facebookGroup")    

    @property
    def instagramId(self):
        return self.getConnect("instagramId")
    
    @property
    def phone(self):
        return self.getConnect("phone")

    @property
    def email(self):
        return self.getConnect("email")        

    @property
    def mastadonURL(self):
        return self.getConnect("mastadonURL")
    
    @property
    def youTubeChannelURL(self):
        return self.getConnect("youTubeChannelURL")
    
    @property
    def youTubeVideoURL(self):
        return self.getConnect("youTubeVideoURL")        

    @property 
    def remoteURL(self):
        return self.getConnect("remoteURL")

    def getConnect(self,arg):
        return self.getJsonValue('connect',arg)

    @property 
    def tiktokId(self):
        return self.getConnect("tiktokId")

    @property 
    def mastodonId(self):
        return self.getConnect("mastodonId")

    def mastodonParts(self):
        id = self.getConnect("mastodonId")
        parts = id.split('@')
        if len(id) == 2:
           return parts 
        else:
            return ("","")

    @property 
    def discordURL(self):
        return self.getConnect("discordURL")
    
class OnlineOrganizationProperties(SocialProperties):
    def getOrganization(self,arg):
        return self.getJsonValue('organization',arg)    

    @property
    def focus(self):
        return (self.getOrganization("focus") or
                self.getIntroduction("focus"))

    @property
    def joinURL(self):
        return self.getOrganiztion("joinURL")

    @property
    def duesURL(self):
        return self.getOrganiztion("duesURL")

    @property
    def eventsPageURL(self):
        return self.getOrganiztion("eventsPageURL")
    
    @property
    def donationsPageURL(self):
        return self.getOrganiztion("donationsPageURL")

    def getHasEvents(self):
        return self.getOrganiztion("hasEvents")    

#LOCATION BASED ORGANIZATIONS HAVE LATTITUDE AND LONGITUDE    
class LocalOrganizationProperties(OnlineOrganizationProperties):
    @property
    def latitude(self):
        return self.getIntroduction("latitude")

    @property
    def longitude(self):
        return self.getIntroduction("longitude")

