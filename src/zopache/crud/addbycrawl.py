from zopache.crud.actions import Add
from zopache.business.interfaces import IOrganization
from bs4 import BeautifulSoup
class AddByCrawl(Add):
    fields = IOrganization
    def __call__(self, form):
        self.form = form
        self.data = form.request['form.field.data']

        soup = BeautifulSoup(html_doc, 'html.parser')
        divs = soup.findAll("div", {"class": "views-rows"})
        for item in divs:
            new.imageURL = item.img.src
            title = item.find("div",{"class":views-field-title})
            title = title.h2.a.content
#views-field-field-website
# .a .urlind_all('a'):

        
    def setFields(self):
            set_fields_data(self.fields, self.new, self.data)
            
    def createItem(self):       
        new = self.new=self.form.factory()
        remoteURL = new.remoteURL
        try:
            result = webp_review(remoteURL, parser="html.parser")
            new.title = result[0]
            new.description = result[1]
            new.imageURL = result[2]
        except:
            error = Error("Failed to Fetch and Parse URL")
            errors.append(error)
        if hasattr(new,'imageURL'):
           self.setimage(imageURL) 
        return Errors()

