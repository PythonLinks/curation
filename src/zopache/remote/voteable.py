import time
from BTrees.OOBTree import OOBTree
class Voteable(object):
    viewCount = 0

    def upVote(self,principal):
        self.possiblyCreateVoteCounts()
        key = principal.__name__
        if key in self._downVotes:
            del self._downVotes[key]
        if key in self._upVotes:
            del self._upVotes[key]
            return
        self._upVotes[key] = time.time()


    def downVote(self,principal):
        self.possiblyCreateVoteCounts()
        key = principal.__name__
        if key in self._upVotes:
            del self._upVotes[key]
        if key in self._downVotes:
            del self._downVotes[key]            
            return
        self._downVotes[key] = time.time()           
        
            
    def possiblyCreateVoteCounts(self):    
        if not hasattr(self,"_upVotes"):
           self._upVotes = OOBTree()
        if not hasattr(self,"_downVotes"):
           self._downVotes = OOBTree()           


    def upVotes(self):
        result = 0
        if hasattr(self,"_upVotes"):
           result += len (self._upVotes)
        if hasattr(self,"likeCount"):
           result += self.likeCount           
        return result

    def downVotes(self):
        result = 0
        if hasattr(self,"_downVotes"):
           result += len (self._downVotes)
        if hasattr(self,"dislikeCount"):
           result += self.dislikeCount           
        return result
    
    def clearVotes(self):
        print(self.__name__)
        #if self.__name__ =='zest-releaser':
        #    breakpoint()
        if hasattr(self,'likeCount'):
            self.likeCount = 0
        if hasattr(self,'dislikeCount'):
            self.dislikeCount = 0
        if hasattr(self,'thumbnails'):
            del self.thumbnails            
            
    def getWilsonScore2(self):
        return self.getWilsonScore()

    def getMyScore2(self):
        return self.getMyScore()
    
    wilsonScore = property (getWilsonScore2)
    myScore = property (getMyScore2)
 
    
