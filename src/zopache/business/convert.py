from zopache.pages.category import Category
from zopache.business.interfaces import IOrganization

class ConvertOrganization (object):
    def moveAttr(self,attrName,targetName, newName = None):
        attrName = newName or attrName
        myDict = self.__dict__
        if attrName in myDict:
           attrValue = myDict[attrName]
           del myDict[attrName]
           if attrValue != "":
               self.json [targetName][attrName] = attrValue

    def convert(self):
        print (self.__name__)        

        self.json = {'introduction':{},
                     'content':[{}],
                     'connect': {},
                     'organization' :{}
                     }
        
        myDict = self.__dict__
        
        self.title = myDict["title"]
        del myDict["title"]
        
        self.description = myDict["description"]
        del myDict["description"]
        
        if "source" in myDict:        
            source = myDict["source"]
            del myDict["source"]
            self.json['content'][0]["source"]  = source
        
        for attribute in [
                 'address',
                 'focus',
                 'longitude'
            ]:
            self.moveAttr(attribute,'introduction')        

        #Facebook    
        self.moveAttr('facebookId','connect',newName = 'facebookGroup')

        value = myDict.get('latitude',None)
        if value == None:
            value = myDict.get('lattitude',None)
            del myDict['lattitude']
        self.json['introduction']['latitude'] = value
        
        for attribute in [                         
                 'remoteURL',
                 'discordURL',
                 'youTubeChannelURL',
                 'phone',
                 'twitterId',
                 'instagramId',
                 'facebookGroup',
                 'facebookPage',
                 'donationsPageURL',
                 'youTubeChannelURL',            
                 'email',
                 'eventsPageURL' ]:
            self.moveAttr(attribute,'connect')
 
          
        for attribute in [                                     
                 'donationsPageURL',
                 'hasEvents',
                 'joinURL',
                 'eventsPageURL',
                   'ballotStatus']:
            self.moveAttr(attribute,'organization')        



class Convert(object):

  def convert(item):
    new = Category()
    parent = item.parent
    newName = item.name
    for attribute in [
                  'name',
                  'parent',
                  'title',
                  'description',
                  'source']:
        setattr(new,attribute,getattr(item,attribute))

        
    for child in item.allValuesAsList():
        childName = child.name
        del item[childName]
        new[childName] = child


    del item.parent[newName]
    parent[newName] = new

