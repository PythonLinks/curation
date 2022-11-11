import urllib


class RedundantNotifications(object):
 
    def getTwitterIds(self,item):
        text = ""
        twitterId = getattr(item,'twitterId','')
        parentTwitterId = getattr(item.parent,'twitterId','')
        # %40 is the @ sign escaped
        if twitterId:
           text += '%40' + twitterId
        if twitterId and parentTwitterId:
           text += '+'
        if parentTwitterId:       
           text += '%40' + parentTwitterId
        return text          

    def getEmails(self,item):
        text = ""
        email = getattr(item,'email','')
        parentEmail = getattr(item.parent,'email','')
        if email:
           text += email
        if email and parentEmail:
           text += ', '
        if parentEmail:       
           text +=  parentEmail
        return urllib.quote_plus(text)
