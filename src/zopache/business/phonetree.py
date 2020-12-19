from zope.interface import implementer
from dataclasses import dataclass
from typing import Any

from zopache.pages.interfaces import IPage
from zopache.pages.page import Page
from zopache.business.iphonetree import ISocialNode,IPhoneTree


class Node(object):
    def __init__(self,instance, facebookGroup, twitterURL, twitterId):
        self.instance = instance
        self.facebookGroup = facebookGroup
        self.twitterURL = twitterURL
        self.twitterId = twitterId

@implementer(IPhoneTree)
class PhoneTree(Page):
    webClass = "SocialNode"
    interface = IPhoneTree
    title = "A Branch of a Phone Tree"
    subtitle = ""
    followers = ""
    leaders = ""
    remoteNodes = ""
    description = "Here are the Twitter Ids for this state."
    webApproved = True

    def childCategories(self):
        result =[]
        for item in self.values():
            if (ISocialNode.providedBy (item) and item.webApproved):
               result.append (item)

        result += self.getRemotePages()
        return result

    def getRemotePages(self):
        return self.remoteObjects(IPage)

    def remoteSocialNodes(self):
        return self.remoteObjects(ISocialNode)
    
    def remoteObjects(self,interface):
        result =[]
        pages = self.remoteNodes.replace("\n"," ")
        pages = pages.replace("\r"," ")        
        pages = pages.split(" ")
        siteRoot = self.getSiteRoot()
        for item in pages:
            if len (item) > 0:
                if item in siteRoot:
                   item = siteRoot[item] 
                   if (interface.providedBy (item) and item.webApproved):
                      result.append (item)
        return result
    
               
        return result


    
    def twitterURLForNode(self,node):
        page = node.instance
        if page:
            return "/" + page.__name__
        else:
            return "https://twitter.com/" + node.twitterId

    def leaderNodes(self):
        leaders = self.convertIdsToArray(self.leaders)
        return self.sort(leaders)

    def getAllFollowersAsString(self):
        followers = self.allFollowerNodes()
        result = ""
        for item in followers:
            result += " " + item.twitterId + ""
        return result
    
    def followerNodes(self):
        followers = self.followers
        followersArray = self.convertIdsToArray(followers)
        return followersArray

    def childFollowerNodes(self):
        childFollowers = ""
        for item in self.values():
            if ISocialNode.providedBy(item):
               childFollowers += " "
               childFollowers += item.leaders
        return self.convertIdsToArray(childFollowers)
    
    def stateFollowerNodes(self):
        stateName = self.remotePages.strip()
        siteRoot = self.getSiteRoot()
        if not stateName in siteRoot:
            return []
        state = siteRoot [stateName]
        result = []        
        for theObject in state.allBlogObjects():
            if (theObject.__class__.__name__ in
                ["Organization","MapOrganization"]):                
                facebookGroup = getattr(theObject,'facebookGroup',"")
                twitterId = getattr(theObject,'twitterId',"")
                twitterURL = ""
                if twitterId:
                    twitterId = "@" + twitterId
                    twitterURL = "/" + theObject.__name__ 
                if facebookGroup or twitterId:                 
                   result.append (Node(theObject,
                                       facebookGroup,
                                       twitterURL,
                                       twitterId))
        return result        

    def allNodes(self):
        leaders = self.leaderNodes()        
        followers = self.followerNodes()
        all = leaders + followers 
        return self.sort(all)

    
    def allFollowerNodes(self):
        followers = self.followerNodes()
        childFollowers = self.childFollowerNodes()
        stateFollowers = self.stateFollowerNodes()
        allFollowers = followers + childFollowers + stateFollowers 
        return self.sort(allFollowers)
        
    def convertIdsToArray(self,aString):
        siteRoot = self.getSiteRoot()
        pagesByTwitterId = siteRoot.pagesByTwitterId
        items = aString.split(" ")
        result = []
        for item in items:
            if len(item) <= 1:
                continue
            item = item [1:]
            if item in pagesByTwitterId:
                theObject =  pagesByTwitterId[item]
                facebookGroup = getattr(theObject,'facebookGroup',"")
                twitterURL = "/" + theObject.__name__
                twitterId = "@" + getattr(theObject,'twitterId',"") 
                result.append (Node(theObject,
                                    facebookGroup ,
                                    twitterURL,
                                    twitterId))
            else:
                 twitterURL = "https://Twitter.com/" + item
                 twitterId =  "@" + item
                 facebookURL = ""
                 result.append(Node(None,
                                    facebookURL,
                                    twitterURL,
                                    twitterId))
        return result



    def sort(self, aList):
        first = []
        second = []
        last = []
        siteRoot = self.getSiteRoot()
        pages = siteRoot.pagesByTwitterId
        for item in aList:
            if item.instance != None:
                if item.twitterId != "":
                   first.append(item)
                else:
                    second.append(item)
            else:
                last.append(item) 
        return first + second + last
    
    def getRemoteNodes(self):
       remoteNodes = self.remoteNodes
       if remoteNodes =="":
           return []
       remoteNodes = remoteNodes.split(" ")
       siteRoot = self.getSiteRoot()
       theObjects = []
       
       for item in remoteNodes:
           if ((len(item)> 0) and
               (item in siteRoot) and
               ISocialNode.providedBy(item)):
                  theObjects.append (siteRoot[item])
       return theObjects
    
@implementer(ISocialNode)
class SocialNode(PhoneTree):
    pass
