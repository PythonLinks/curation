from zopache.crud.actions import Add

from zopache.crud.update import  Update

class AddAndCkEdit(Add):
    def newURL(self,baseURL):
       return self.appendName(baseURL,"ckedit")        
        
class AddAndAceEdit(Add):
    def newURL(self,baseURL):
       return self.appendName(baseURL,"aceedit")        

class AddAndSearch(Add):
    def newURL(self,baseURL):
       return self.appendName(baseURL,"search")                

class AddAndViewSource(Add):
    def newURL(self,baseURL):
       return self.appendName(baseURL,"viewsource")             

class AddAndManage(Add):
    def newURL(self,baseURL):
       return self.appendName(baseURL,"manage")            

class SaveAndCkEdit(Update):
    def newURL(self,baseURL):
       return self.appendName(baseURL,"ckedit")
   
class SaveAndAceEdit(Update):
    def newURL(self,baseURL):
       return self.appendName(baseURL,"aceedit")        


    
