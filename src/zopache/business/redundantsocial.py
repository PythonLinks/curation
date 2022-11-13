
class RedundantSocial(object):
 
    def redundantTwitterIds(self):
        text = ""
        twitterId = getattr(self,'twitterId','')
        parentTwitterId = getattr(self.parent,'twitterId','')
        # %40 is the @ sign escaped
        if twitterId:
           text += '%40' + twitterId
        if twitterId and parentTwitterId:
           text += '+'
        if parentTwitterId:       
           text += '%40' + parentTwitterId
        return text

    #JUST ONE
    def redundantTwitterId(self):
        text = ""
        twitterId = getattr(self,'twitterId','')
        parentTwitterId = getattr(self.parent,'twitterId','')
        if twitterId:
           text +=  twitterId
        elif parentTwitterId:       
           text +=  parentTwitterId
        return text              

    def redundantEmails(self):
        text = ""
        email = getattr(self,'email','')
        parentEmail = getattr(self.parent,'email','')
        if email:
           text += email
        if email and parentEmail:
           text += ', '
        if parentEmail:       
           text +=  parentEmail
        return text

    def redundantRemoteURL(self):
        text = ""
        value = getattr(self,'remoteURL','')
        parentValue = getattr(self.parent,'remoteURL','')
        if value:
           text += value
        elif parentValue:       
           text +=  parentValue
        return text

    def redundantJoinURL(self):
        text = ""
        value = getattr(self,'joinURL','')
        parentValue = getattr(self.parent,'joinURL','')
        if value:
           text += value
        elif parentValue:       
           text +=  parentValue
        return text

    def redundantPhone(self):
        text = ""
        value = getattr(self,'phone','')
        parentValue = getattr(self.parent,'phone','')
        if value:
           text += value
        elif parentValue:       
           text +=  parentValue
        return text    
    


    def redundantYouTubeChannelURL(self):
        text = ""
        value = getattr(self,'youTubeChannel','')
        parentValue = getattr(self.parent,'youTubeChannelURL','')
        if value:
           text += value
        elif parentValue:       
           text +=  parentValue
        return text
    
    
