from dolmen.forms.base import Action, SuccessMarker
from zopache.core.transactionnote import TransactionNote
from dolmen.forms.base.markers import FAILURE
from cromlech.browser import IURL
from zopache.core.getroot import getSiteRoot
from zope.location import ILocation

class DeleteAction(Action):
    """Delete action for any locatable context.
    """
    successMessage = (u"The object has been deleted.")
    failureMessage = (u"This object could not be deleted.")

    def available(self, form):
        content = form.getContentData().getContent()
        if ILocation.providedBy(content):
            container = content.__parent__
            return (hasattr(container, '__delitem__') and
                    hasattr(container, '__contains__'))
        return False

    def __call__(self, form):
        content = form.getContentData().getContent()

        if ILocation.providedBy(content):
            container = content.__parent__
            name = content.__name__
            if name in container:
                try:
                    item = container[name]
                    root = getSiteRoot(item)
                    products = form.getProducts()
                    del container[name]
                    root.indexTree()
                    products.indexTree()
                    form.status = self.successMessage
                    form.message(form.status)
                    url = str(IURL(container, form.request))
                    url = url + '/manage'
                    return SuccessMarker('Deleted', True, url=url)
                except ValueError:
                    pass

        form.status = self.failureMessage
        form.message(form.status)
        return FAILURE
