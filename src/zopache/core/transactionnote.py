
import transaction

class TransactinNote(object):
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
    
    
