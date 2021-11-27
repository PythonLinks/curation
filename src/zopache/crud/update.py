from dolmen.forms.base import Action, SuccessMarker
from zopache.core.transactionnote import TransactionNote
from dolmen.forms.base.markers import FAILURE
from dolmen.forms.base.utils import set_fields_data, apply_data_event
from zopache.crud import i18n as _
from zopache.crud.actions import Cancel
from zopache.pages.page import Page

class Update(Action,TransactionNote):
    """Update action for any locatable object.
    """


    """
        import cProfile, pstats
        profiler = cProfile.Profile()
        profiler.enable()
        
        self.callInner(form)
        
        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('cumtime')
        stats.print_stats()
    """
    
    def __call__(self, form):
        self.form=form
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE
        context = form.context
        if hasattr(context, "preProcess"):
           context.preProcess(form)        
        if hasattr(form,'applyData'):
           form.applyData(data)
        else:   
           apply_data_event(form.fields, form.getContentData(), data)
        #form.message(_(u"URL updated"))
        if hasattr(form,'postProcess'):        
               form.postProcess(view = form)
        elif hasattr(form.context,'postProcess'):
               form.context.postProcess(view=form)
        baseURL = self.form.absoluteURL()
        url=self.newURL(baseURL)
        self.describeWithView(form.context,form)
        if url == form.request.url:
           return SuccessMarker('Updated', True)
        else:
           return SuccessMarker('Updated', True, url=url)

    def appendName(self,baseURL,name):
        if baseURL == "":
           baseURL = "/"
        elif baseURL [-1] != "/":
            baseURL += "/"
        baseURL += name
        return baseURL

    def newURL(self,baseURL):
        if hasattr(self.form, 'newURL'):
            return self.form.newURL(baseURL)
        else:
           result = self.appendName(baseURL,getattr(self.form,"crom.name"))
           return result

    def postProcess(self):
            pass


            
#JUST TO MAKE IT EASIER TO UNDERSTAND        
class Edit(Update):
    pass

class Save(Update):
    pass
    
class SaveAndView(Update):
        def newURL(self,baseURL):
               return baseURL

class SaveAndViewHTML(Update):
        def newURL(self,baseURL):
               return baseURL + '/html'

class SaveAndViewJS(Update):
        def newURL(self,baseURL):
               return baseURL + '/javascript'

class SaveAndRoot(Update):
    def newURL(self,baseURL):
        return "/"

class SaveAndParent(Update):
    def newURL(self,baseURL):
        return ".."    

class SaveAndTest(Update):
        def newURL(self,baseURL):
               return self.form.context.testURL

class SaveAndViewURL(Update):
      def newURL(self,baseURL):
          return self.form.newURL(baseURL)
    
