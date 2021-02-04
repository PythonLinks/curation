
"""class NotUsed():
    def extractSocialMediaLinks(self,response):
         tree = parse_html_bytes(response.content,
                    response.headers.get('content-type'))
         links = set(find_links_tree(tree))
         remainingLinks = []
         
         for url in links:
             if 'facebook.com/group/' in url:
                 self.processURL(self,url,'facebookGroup',
                                 'acebook.com/group/')
                 continue
             if 'facebook.com/' in url:
                  self.processURL(self,url,'facebookId',
                                 'acebook.com/')
                  continue
             if 'twitter.com/' in url:  
                  self.processURL(self,url,'twitterId',
                                 'witter.com/')
                  continue              
             if 'twitter.com/intent/follow?screen_name=' in url:  
                  self.processURL(self,url,'twitterId',
                    'witter.com/intent/follow?screen_name=')
                  continue
             if 'twitter.com/' in url:  
                  self.processURL(self,url,'twitterId',
                                 'witter.com/')
                  continue              
             if 'youtube.com/channel' in url:  
                  self.processURL(self,url,'youtubeId',
                                 'youtube.com/channel/')
                  continue
             if 'youtube.com/user' in url:  
                  self.processURL(self,url,'youtubeId',
                                 'youtube.com/user/')
                  continue
             if 'youtube.com/' in url:  
                  self.processURL(self,url,'youtubeId',
                                 'youtube.com/')
                  continue                            
             if 'instagram.com/' in url:  
                  self.processURL(self,url,'instagramId',
                                 'stagram.com/')
                  continue
             remainingLinks.append(url)
                 
         allLinks = []       
         for item in remainingLinks:                                
              oneLink = self.href(item,item)
              allLinks.append(oneLink)                    
              self.new.source = '<br>'.join(allLinks)
"""
