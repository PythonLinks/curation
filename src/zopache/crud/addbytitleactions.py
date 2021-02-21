from zopache.crud.actions import AddByTitle

__all__ = ['AddByTitleAndAceEdit',
           'AddByTitleAndCkEdit',
           'AddByTitleAndView',
           'AddByTitleAndManage']

class AddByTitleAndView(AddByTitle):
    def newURL(self,baseURL):
        return baseURL 

class AddByTitleAndCkEdit(AddByTitle):
    def newURL(self,baseURL):
        return baseURL + '/ckedit'    

class AddByTitleAndAceEdit(AddByTitle):
    def newURL(self,baseURL):
        return baseURL + '/aceedit'

class AddByTitleAndManage(AddByTitle):
    def newURL(self,baseURL):
        return baseURL + '/manage'
