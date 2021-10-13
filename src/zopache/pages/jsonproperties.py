#uSED TO CREATE A SIMPLE INTERFACE TO SOCIAL DATA FOR JSON SCHEMA OBJECTS

#FIRST the Basics TITLE, DESCRIPTION, SOURCE
class BasicProperties(object):
    @property
    def title(self):
        return self.json['content'][0]["title"]

    @property
    def description(self):
        return self.json['content'][0].get("description","")

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
    def facebookURL(self):
        return self.getConnect("facebookURL")

    #THIS NEEDS TO BE RETIRED EVENTUALLY
    @property
    def facebookId(self):
        return self.getConnect("facebookURL")    

    #THIS ONE NEEDS TO BE RETIRED EVENTUALLY
    @property
    def facebookGroup(self):
        return self.getConnect("facebookGroupURL")

    @property
    def facebookGroupURL(self):
        return self.getConnect("facebookGroupURL")    

    @property
    def facebookURL(self):
        return self.getConnect("facebookURL")

    @property
    def instagramURL(self):
        return self.getConnect("instagramURL")

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
    def youTubeURL(self):
        return self.getConnect("youTubeURL")    

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
    def getOrganizaiton(self,arg):
        return self.getJsonValue('organization',arg)    

    @property
    def focus(self):
        return self.getIntroduction("focus")

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

