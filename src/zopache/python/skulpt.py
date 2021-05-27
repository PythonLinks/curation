import json
import transaction

from dolmen.view import View
from cromlech.webob.response import Response
from dolmen.view import View, make_view_response
from dolmen.forms.base import Actions
from dolmen.forms.base.errors import Error
from dolmen.container import IBTreeContainer ,OrderedBTreeContainer
from dolmen.forms.base import DISPLAY

from zopache.pages.page import Page
from zopache.core import Leaf
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.core.transactionnote import TransactionNote
from zopache.ttw.interfaces import IJSON, IJSONContainer
from zopache.ttw.acescripts import AceScripts
from zopache.ttw.javascript import JavascriptBase
from zopache.core.interfaces import ITreeSecurity
from zopache.core.viewdecorators import *
from zopache.core import Container
from zopache.pages.interfaces import IPage
from zopache.crud.update import Edit
from zopache.crud.forms import AddByTitle, EditForm
from zopache.python.iskulpt import ISkulptSolution, ISkulptAssignment
from zopache.crud import update as editactions                    

@implementer(ISkulptSolution)
class Solution(Leaf):
    icon="ttwicons/Python.svg"
    _solutionCode = ""
    comments = ""
    result = ""
    def className(self):
        return self.__class__.__name__
    
    @property
    def title (self):
        return  self.parent.title

    @property
    def description(self):
        return self.parent.description

    @property
    def problemText(self):
        return self.parent.problemText
    
    @property
    def problemCode(self):
           return self._code or self.parent.problemCode

    @property
    def solutionText(self):
        return self.parent.solutionText

    @property
    def timeIsUp(self):
        return self.parent.timeIsUp
    
    @property
    def showSolution(self):
        return self.parent.showSolution
    
    def getProblemCode(self):
       return self._code or self.parent.problemCode
 
    def setProblemCode(self,value):
        self._code = value

    problemCode = property (getProblemCode, setProblemCode)

@implementer(ISkulptAssignment)
class SkulptAssignment(Page):
    webClass = "Skulpt"
    icon="ttwicons/Python.svg"
    title = ""
    description = ""
    problemText = ""
    timeIsUp = False
    showSolution = False
    problemCode ="""#Please complete this program to solve the problem.
def run():
"""
    solutionText = ""
    solutionCode = ""
    showSolution = False
    answer = ""

    def studentsWork(self,view):
        principal = view.request.principal
        handle = principal.title
        if not handle in self:
            self[handle]= new = Solution()
            new._code = self.problemCode
            msg = handle +" Answered: " + self.title
            TransactionNote().describeTransactionWithText(msg)
            transaction.commit()
        return self[handle]

from zopache.crud.forms import AddByTitleForm
from dolmen.forms.base import Fields
from zopache.ttw.htmlviews import CkScripts


def skulptScripts():    
         return """
         <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js" type="text/javascript"></script> 
<script src="/root/Products/Templates/Skulpt/skulpt.min.js" type="text/javascript"></script> 
<script src="/root/Products/Templates/Skulpt/skulpt-stdlib.js" type="text/javascript"></script> 
<script src="/root/Products/Templates/Skulpt/fiddle.js" type="text/javascript"></script> 

<script src="/root/Products/Templates/Skulpt/addButtons" type="text/javascript"></script> 

"""

     
class SharedForm(TransactionNote,AceScripts,CkScripts):
    aceMode = "python"
    actions = Actions()
    layoutName = "UserMenu"

    def update(self):

        self.template = self.getTemplates()['Skulpt']

    def isTeacher(self):
        return self.isManager()

    def isAnonymousVisitor(self):
        return not self.isAuthenticated()    
        
    def headerScripts(self):
        return CkScripts.headerScripts(self) + AceScripts.headerScripts(self)

    def isTeacherOrShowSolution(self):
        return self.isTeacher() or self.context.showSolution

class AssignmentForm(SharedForm):
    fields = Fields(ISkulptAssignment)
    def footerScripts(self):

         result = """ <script>
         createAce("form-field-problemCode","python");
         listenForErrors();
           """

         if self.isTeacher():
            result +=""" 
        CKEDITOR.replace('form-field-problemText',
       {disableNativeSpellChecker : false}); 
        CKEDITOR.replace('form-field-solutionText',
       {disableNativeSpellChecker : false}); 
         """

         if self.isTeacherOrShowSolution():
             result += """ 
           createAce("form-field-solutionCode","python");
           """
         result += """    
         const form = document.getElementById('form');
         form.addEventListener('submit', saveThenSubmit);    
         </script>"""
         return result

    def getContent(self):
        if self.isStudent():
            return self.context.studentsWork(self)
        else:
            return self.context
        
    @property        
    def title(self):
        if self.isTeacher():
           return "Edit a Python (Skulpt) Assignment"
        else:
           return self.context.title
       
    def isStudent(self):
        if self.isAuthenticated() and not self.isManager():
           return True
        return False
    
    def update(self):
        
        isAnonymous = self.isAnonymousVisitor()
        isTeacher = self.isTeacher()
        isStudent = self.isStudent()

        if not isTeacher:
            self.fields["title"].mode = DISPLAY
           
        if not isTeacher:
            self.fields["problemText"].mode = DISPLAY
            self.fields["solutionText"].mode = DISPLAY            

        if isTeacher or isAnonymous:
            self.fields = self.fields.omit('comments')
        sharedForm.update()
    
class SolutionForm(SharedForm):
    fields = Fields(ISkulptSolution)
    
    def footerScripts(self):
         result = """ <script>
         createAce("form-field-problemCode","python");
        CKEDITOR.replace('form-field-comments',
       {disableNativeSpellChecker : false}); 
         const form = document.getElementById('form');
         form.addEventListener('submit', saveThenSubmit);    
         </script>"""
         return result
    
    def update(self):
        isTeacher = self.isTeacher()
        isTheStudent = self.request.principal == self.context.name
        if not (isTeacher or isTheStudent):
            self.raiseUnauthorized()
            

        #We are overriding the Edit form actions
        #So call it before hte override
        EditForm.update(self)        
        if isTeacher or isTheStudent:
            self.actions = Actions(editactions.Edit("Save","Save"),
                    editactions.SaveAndView("SaveAndView","Save And View"),
                    editactions.Cancel("Cancel","Cancel"))
            
        #Must be after Edit Form    
        SharedForm.update(self)          
     
@view_component
@name('addAssignment')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddAssignment(AssignmentForm,AddByTitle):
    title = 'Create a Python (Skulpt) Assignment'
    subTitle= ""
    ignoreContent = True
    factory = SkulptAssignment
    schemaName = "AssignmentSchema"
    interface = ISkulptAssignment
    aceMode = "python"
    def update(self):
        AddByTitleForm.updateWidgets(self)    
        AssignmentForm.update(self)        

@form_component
@context(ISkulptAssignment)
@name("index")
class AceEditSkulptAssignment(AssignmentForm,EditForm):
    schemaName = "AssignmentSchema"
    title = "Class Assignment"
    subTitle = "Work on a class ssignment2"
    title = ""
    subTitle = ""
    interface = ISkulptAssignment
    
    def update(self):
        isAnonymous = self.isAnonymousVisitor()
        isTeacher = self.isTeacher()
        isStudent = self.isStudent()

        #We are overriding the Edit form actions
        #So call it before hte override
        EditForm.update(self)        
        if isTeacher or isStudent:
            self.actions = Actions(editactions.Edit("Save","Save"),
                    editactions.SaveAndView("SaveAndView","Save And View"),
                    editactions.Cancel("Cancel","Cancel"))
        #Must be after EditForm.update()
        SharedForm.update(self)          

        
        if not self.context.showSolution and not isTeacher:
             self.fields = self.fields.omit('solutionText')
             self.fields = self.fields.omit('solutionCode')             
   
        if not isTeacher:
            self.fields = self.fields.omit('showSolution')
           
        if self.context.showSolution:
           if not isTeacher:
               self.fields['solutionText'].mode = DISPLAY
               self.fields['solutionCode'].mode = DISPLAY                      
        else:
           if not isTeacher:           
               self.fields = self.fields.omit('solutionText')
               self.fields = self.fields.omit('solutionCode')           
        #AceEditForm.updateWidgets(self)              

    def addUnauthorizedActions(self):
        self.actions = Actions()
        
    def addAuthorizedActions(self):
        if self.isTeacher() or self.isStudent():
           self.actions = Actions(
               Edit("Save","Save"))
           
    def extractData(self):
        data, errors = AceEditForm.extractData(self)
        if self.context.timeIsUp and not self.isTeacher():
            errors += Error("Time is up, no more submissions.")
        return data, errors

    def applyData(self,data):
        context = self.context
        if self.isTeacher():
           context.title = data['title'] 
           context.problemText = data['problemText']
           context.problemCode = data['problemCode']           
           context.solutionText = data['solutionText']
           context.solutionCode = data['solutionCode']           
           context.showSolution = data['showSolution']
           context.timeIsUp=data['timeIsUp']           
           msg = "Teacher edited: " + self.title
           self.describeTransactionWithText(msg)
           
        else:
           answer = self.context.studentsWork(self) 
           answer.comments = data['comments']
           answer.problemCode = data['problemCode']

#NOW FOR EDITING STUDENT SOLUTIN
@form_component
@context(ISkulptSolution)
@name("index")
class AceEditSkulptSolution(SolutionForm, EditForm):
    title = "Students's Work"
    subTitle = ""
    interface = ISkulptSolution
    

    def addAuthorizedActions(self):
        if self.isTeacher() or self.isStudent():
           self.actions = Actions(
               Edit("Save","Save"))
           
    def applyData(self,data):
        context = self.context
        context.comments = data['comments'] 
        context.problemCode = data['problemCode']           
        if self.isTeacher():
           msg = "Teacher edited: " + self.title
        else:
           msg = "Student  edited: " + self.title            
        self.describeTransactionWithText(msg)


@form_component
@context(ISkulptAssignment)
@name("asStudent")
@implementer(ITreeSecurity)
class AsStudent(AceEditSkulptAssignment):           
    def isTeacher(self):
       return False
    def isStudent(self):
       return True

@form_component
@context(ISkulptAssignment)
@name("asAnonymous")
@implementer(ITreeSecurity)
class AsAnonymous(AceEditSkulptAssignment):           
    def isTeacher(self):
       return False
    def isAnonymousVisitor(self):
       return True
