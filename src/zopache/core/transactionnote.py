
import transaction
from cromlech.security import unauthenticated_principal as anonymous

class TransactionNote(object):
    def describeTransactionWithText(self,text):
        transaction.get().note(text)

    def describeTransaction(self,type, item=None):        
         note = type + ' ' + item.__name__ + " "
         note += "<br>"
         transaction.get().note(note)

    def describeTransactionWithTitle(self,type, item):        
         note = type + ' ' + item.__name__ + " "
         try:
             note +=item.title
         except:
             pass
         note += "<br>"
         transaction.get().note(note)
    
    def describeWithView(self,item,view):
        action =  view         
        self.describeWithActionAndView (item,action,view)
        
    def describeWithActionAndView (self,item,action,view):
         thisTransaction = transaction.get()
         user = view.request.principal
         if user == anonymous:
            userId = 'Anonymous'
            userName = 'Anonymous'
         else:
            userId = user.__name__
            userName = user.title
         thisTransaction.setUser(userId)
         thisTransaction.note(userName + ' ')
         
         note = action.__class__.__name__ + ' '
         note += item.__name__ + ' '
         
         try:
             note +=item.title
         except:
             pass
         note += "<br>"

         thisTransaction.note(note)
