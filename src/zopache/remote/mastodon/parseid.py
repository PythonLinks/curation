
class ParseMastodonId(object):
    @property
    def remoteURL(self):
        blank,user, server = self.parts()
        return 'https://' + server + '/@' + user

    def getLink(self):
        return f'<a href ="{self.remoteURL}">{self.userName()}</a>'
        
    def parts(self):
        id = self.mastodonId
        if id[0]!='@':
            id = '@' + id
        return id.split('@')

    def userName(self):
        return "@" + self.parts()[1]
    
