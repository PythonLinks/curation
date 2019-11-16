from zopache.ttw.acquisition import ParentalAcquire,webClassAcquire


class Acquisition(object):

    #THIS ONE IS BEING DEPRECATED
    #NOT QUITE CLEAR WHAT IT DOES
    def acquire(self,name, context=None):
        return self.parentalAcquire(name,context)
      
    def parentalAcquire (self,name,context=None):  
            if (context == None):
               context = self
            return ParentalAcquire(context)[name]
          
    def webClassAcquire(self,name,context=None):
        if context == None:
           context = self.context
        return webClassAcquire(context,name)   

    def acquireTitle(self):
        if (hasattr(self.context,"webClass") and
            (self.context.webClass == "Company") and
            not self.isAuthenticated()):
              return "Please login to see the Company"
        if hasattr(self,'title'):
           return self.title
        return self.acquireAttribute('title')

    def acquireAttribute(self, attribute):      
        parents = self.lineage(self.context)
        for item in parents:
            result = getattr(item,attribute,'')
            if result:
               return result
        return ''

    
    #QUITE A STRANGE METHOD.  DO I REALLY USE IT?
    def safeParentalAcquire(self,name,context=None):
          if context==None:
             context = self.context

          result = ParentalAcquire(context) [name]
          if result == None:
             return ("ERROR: " + name +
                     "DOES NOT EXIST IN THE PARENTS OF" +
                     self.href(self.url(context), context.name))
          try:
              result = result (self)
              return result
          except:
            return "ERROR IN SAFE PARENTAL ACQUIRE"

    def templateParentalAcquire(self, name):
        result = ParentalAcquire(self.zopacheTemplate)
        return result [name]
