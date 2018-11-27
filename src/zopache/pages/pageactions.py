from zopache.crud.actions import AddByTitle

__all__ = ['AddAndAceEdit','AddAndCkEdit','AddAndView','AddAndManage']

class AddAndView(AddByTitle):
    def newURL(self,baseURL):
        return baseURL 

class AddAndCkEdit(AddByTitle):
    def newURL(self,baseURL):
        return baseURL + '/ckedit'    

class AddAndAceEdit(AddByTitle):
    def newURL(self,baseURL):
        return baseURL + '/aceedit'

class AddAndManage(AddByTitle):
    def newURL(self,baseURL):
        return baseURL + '/manage'
