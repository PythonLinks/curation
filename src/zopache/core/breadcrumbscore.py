from cromlech.browser import IPublicationRoot
from zopache.crud.interfaces import IZodbRoot


class BreadcrumbsCore(object):


    #AND HERE WE HAVE THE WORKHORSE                
    def breadcrumbsCore(self,
                        item,
                        viewName='',
                        showTitles=True,
                        showRoot=True
                        ):

        if showRoot:
           parents = self.parentsUpToZodbRoot(item=item)
        else:    
           parents = self.parentsUpToSiteRoot(item=item)        
        
        result=[]
        if parents:
            for ancestor in parents:
                name, title = self.nameAndTitle(ancestor,showTitles)
                slashViewName = self.slashViewName(ancestor,viewName)
                base_url = self.getLongURL(ancestor)
                newURL= base_url + slashViewName
                result.append( self.href(newURL,title))
        return ' / '+' / '.join(result)
             
    def divBreadcrumbs(self, node,viewName ='',widget= False,start = 0):
        items = self.parentsUpToSiteRoot()
        items = items [start:]
        length = len(items)
        if length > 50:
            return "ERROR IN DIV BREADCRUMBS"
        result= '<div style = "text-align:left; ">'
        target = False
        indent = -1
        for step,item in enumerate(items):
                   if widget and step > 0 and (step < length -3):
                       continue
                   if widget and (step == length -2):
                       continue                     
                   indent += 1
                   result += '<div style = "margin-left:' 
                   result +=  str(indent) + 'em">'
                   target = False
                   if widget:
                     if step == 0:
                         viewName = ''
                         target = True                        
                     if step == length -1:
                        viewName = 'showvideo'
                     if step == length -3:
                        viewName = 'videos'                        
                   slashViewName = self.slashViewName(item,viewName)
                   result += self.href(('/' + item.__name__ + slashViewName),
                                           item.title,
                                           target=target)
                   result +=  ' &nbsp;(' + str(item.branchSize) + ')'
                   result +=  '</div>'
        result += "</div>"
        return result
    
    def breadcrumbsIndex(self,item):
        return self.breadcrumbsView(item,viewName='',showTitles=True)

    #THE DEFAULT BREADCRUMBS
    def breadcrumbs(self):
        return self.breadcrumbsIndex(self.context)
          
    #FOR MANAGEMENT VIEWS  
    def breadcrumbsManage(self):
        return self.breadcrumbsView(self.context,viewName='manage',showTitles=False)

    #SKIP THE CURRENT OBJECT, IF POSSIBLE
    def breadcrumbsParent(self):
        if IPublicationRoot.providedBy(self.context):
            return self.breadcrumbsIndex(self.context)
        else:
            return self.breadcrumbsIndex(self.context.__parent__)          

    #LEGACY VERSION,
    #COULD BE RETIRED
    def breadcrumbsView(self,item, viewName='',showTitles=True):
        return  self.breadcrumbsCore(item,
                                     viewName=viewName,
                                     showTitles=showTitles)
        if showRoot:
           parents = self.parentsUpToZodbRoot(item=item)
        else:    
           parents = self.parentsUpToSiteRoot(item=item)        
        
        result=[]
        if parents:
            for ancestor in parents:
                name, title = self.nameAndTitle(ancestor,showTitles)
                slashViewName = self.slashViewName(ancestor,viewName)
                base_url = self.getLongURL(ancestor)
                newURL= base_url + slashViewName
                result.append( self.href(newURL,title))
        return ' / '+' / '.join(result)
             
    def divBreadcrumbs(self, node,viewName ='',widget= False,start = 0):
        items = self.parentsUpToSiteRoot()
        items = items [start:]
        length = len(items)
        if length > 50:
            return "ERROR IN DIV BREADCRUMBS"
        result= '<div style = "text-align:left; ">'
        target = False
        indent = -1
        for step,item in enumerate(items):
                   if widget and step > 0 and (step < length -3):
                       continue
                   if widget and (step == length -2):
                       continue                     
                   indent += 1
                   result += '<div style = "margin-left:' 
                   result +=  str(indent) + 'em">'
                   target = False
                   if widget:
                     if step == 0:
                         viewName = ''
                         target = True                        
                     if step == length -1:
                        viewName = 'showvideo'
                     if step == length -3:
                        viewName = 'videos'                        
                   slashViewName = self.slashViewName(item,viewName)
                   result += self.href(('/' + item.__name__ + slashViewName),
                                           item.title,
                                           target=target)
                   result +=  ' &nbsp;(' + str(item.branchSize) + ')'
                   result +=  '</div>'
        result += "</div>"
        return result
    
    def breadcrumbsIndex(self,item):
        return self.breadcrumbsView(item,viewName='',showTitles=True)

    #THE DEFAULT BREADCRUMBS
    def breadcrumbs(self):
        return self.breadcrumbsIndex(self.context)
          
    #FOR MANAGEMENT VIEWS  
    def breadcrumbsManage(self):
        return self.breadcrumbsView(self.context,viewName='manage',showTitles=False)

    #SKIP THE CURRENT OBJECT, IF POSSIBLE
    def breadcrumbsParent(self):
        if IPublicationRoot.providedBy(self.context):
            return self.breadcrumbsIndex(self.context)
        else:
            return self.breadcrumbsIndex(self.context.__parent__)          

    #LEGACY VERSION,
    #COULD BE RETIRED
    def breadcrumbsView(self,item, viewName='',showTitles=True):
        return  self.breadcrumbsCore(item,
                                     viewName=viewName,
                                     showTitles=showTitles)
