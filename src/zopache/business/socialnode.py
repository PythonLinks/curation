from zopache.business.iphonetree import ISocialNode
from zopache.business.phonetree import PhoneTree
from zope.interface import implementer

@implementer(ISocialNode)
class SocialNode(PhoneTree):
    pass
