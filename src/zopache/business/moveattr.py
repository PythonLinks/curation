

def moveAttr(self,attrName,dictName, array = False, newName = None):
        newAttrName = newName or attrName
        if attrName in self.__dict__:
           attrValue = self.__dict__[attrName]
           del self.__dict__[attrName]
           if attrValue != "":
               if not dictName in self.json:
                 if array:
                   self.json[dictName] = []
                   self.json[dictName].append(dict())
                 else:  
                   self.json[dictName] = dict()
               sub =  self.json[dictName] 
               if array:
                  sub = sub [0]    
               sub [newAttrName] = attrValue


class Convert(object):
   def convert(self):
        self.convertCore()

       
   def convertCore(self):
      if not hasattr(self,'json'):
          self.json = dict()
      else:
          raise Exception(f"This   object {self.name} was already converted.")
      self._p_changed = True
      for key in [ "donationPageURL","url"]:
          if key in self.__dict__:
              del self.__dict__[key]
      keys = []
      for key,value in self.__dict__.items():
          if key not in [
                          '__implemented__',
                          '_members',
                          'members',
                          'editors',
                          'private',
                          'hidden',          
                          '_data',
                          '_BTreeContainer__len',
                          '_order',
                          'creationTime',
                          'emailApproved',          
                          'modificationTime',
                          'registerURL',
                          'isGlobal',
                          '__parent__',
                          '__name__',
                          'webApproved',
                          'createdBy',
                          'editedBy',
                          'json']:
                  keys.append(key)

      for key in keys:        
          if key   in [
                         "focus",        
                         "address",
                         "latitude",
                         "longitude"]:
                 moveAttr(self,key,"introduction")
                  
          elif key in [
                          "title",
                          "description",
                          "source" ]:
                 moveAttr(self,key,"content", array = True)
          
          elif key in ["duesURL",
                       "ballotStatus",
                       "joinURL", #Join the Organization
                       "eventsPageURL",
                       "hasScheduledEvents",
                       "donationsPageURL"]:
                 moveAttr(self,key,"organization")
  
          elif key in [
                    "twitterId",
                    "phone",
                    "instagramId",
                    "remoteURL",
                    "facebookId",
                    "facebookGroup",
                    "youTubeChannelURL",
                    "email"]:
                 moveAttr(self,key,"connect")
          else:
              raise Exception("No such attribute")
          
                


