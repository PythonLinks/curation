from zopache.crud.actions import Add, Update

class AddAndCkEdit(Add):
    def newURL(self,baseURL):
        return baseURL + '/ckedit'

class AddAndAceEdit(Add):
    def newURL(self,baseURL):
        return baseURL + '/aceedit'
 
class AddAndSearch(Add):
    def newURL(self,baseURL):
        return baseURL + '/search'   

class AddAndViewSource(Add):
    def newURL(self,baseURL):
        return baseURL + '/viewsource'    
    
class AddAndManage(Add):
    def newURL(self,baseURL):
        return baseURL + '/manage'

class SaveAndCkEdit(Update):
    def newURL(self,baseURL):
        return baseURL + '/ckedit'

fred = """



"""    
    
class SaveAndAceEdit(Update):
    def newURL(self,baseURL):
        return baseURL + '/aceedit'                


    
