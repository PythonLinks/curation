import feedparser

from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.remote.rssdownload import getRSS
from zopache.pages.interfaces import IPage
from zopache.remote.rss import IRSS



@form_component
@context(IPage)
@crom.target(IView)
@name("getrss")
@permissions('Manage')
class GetRSS(Form):
    title = "Download the RSS Feeds"
    subTitle = "To get the newest news."
    def update(self):
           urls = []
           feedsByURL = {}
           for item in self.context.allBlogObjects():
               if IRSS.providedBy(item):
                   rssURL =  item.rssURL
                   urls.append (rssURL)
                   feedsByURL [rssURL] = item

           result = getRSS(urls)
           for key, value in result.items():
               feed = feedsByURL [key]
               feed.createArticles(value,self)
           self.status='RSS Feeds were downloaded.'
           Form.update(self)

