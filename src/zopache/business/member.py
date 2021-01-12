

class Member(object):
    subscriber = False
    endorser = False
    donor = False
    volunteer = False
    
    def __init__(self,name):
        self.__name__ = name

    def isActive(self):
        return (self.subscriber or
                self.endorser or
                self.donor or
                self.volunteer)
