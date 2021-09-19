
from html_to_etree import parse_html_bytes
from extract_social_media import find_links_tree
 
class SocialMediaExtractor(object):
    def addToConnect(self,connect,url,key,pattern):
        if pattern in url:
           connect[key] = url
    
    def addSocialMedia(self,connect, response):
         tree = parse_html_bytes(response.content,
                    response.headers.get('content-type'))
         links = set(find_links_tree(tree))
         
         for url in links:
             if 'facebook.com/group/' in url:
                 connect['facebookGroup'] = url

             elif 'facebook.com/' in url:
                  connect['facebookPage'] = url

             elif 'twitter.com/intent/follow?screen_name=' in url:  
                  parts = url.split('twitter.com/intent/follow?screen_name=')
                  connect['twitterId'] = parts [1]
                  
             elif 'twitter.com/' in url:  
                  parts = url.split('twitter.com/')
                  connect['twitterId'] = parts [1]                  

             elif 'youtube.com/' in url:  
                  self.addToConnect(connect, url,'youTubeChannelURL',
                                 'youtube.com/')

             elif 'instagram.com/' in url:  
                  self.addToConnect(connect, url,'instagramId',
                                 'stagram.com/')

