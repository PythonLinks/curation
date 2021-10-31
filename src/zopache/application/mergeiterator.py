#!/usr/bin/env python

"""An extended example of generators in action.  Provides a function
called mergeiter that merges two iterators together.

Danny Yoo (dyoo@hkn.eecs.berkeley.edu)
"""

from __future__ import generators


def mergeiterator(i1, i2, cmp):
    """Returns the "merge" of i1 and i2.  i1 and i2 must be iteratable
    objects, and we assume that i1 and i2 are both individually sorted.
    """

    left, right = ExtendedIter(i1), ExtendedIter(i2)
    while 1:
        if not left.has_next():
            while right.has_next():
                 yield right.next()
            return None
        elif not right.has_next():
            while left.has_next():
                 yield left.next()
            return None
        
        comparison = cmp(left.peek(), right.peek())
        if comparison < 0:
            yield  left.next()
        elif comparison == 0:
            yield  left.next()
            yield  right.next()
        else:
            yield right.next()

class ExtendedIter:
    """An extended iterator that wraps around an existing iterators.
    It provides extra methods:

        has_next(): checks if we can still yield items.

        peek(): returns the next element of our iterator, but doesn't
                pass by it."""
    def __init__(self, i):
        self._myiter = iter(i)
        self._next_element = None
        self._has_next = 0
        self._prime()

    def has_next(self):
        return self._has_next


    def peek(self):
        assert self.has_next()
        return self._next_element


    def next(self):
        "Returns the next element in our iterator."
        if not self._has_next:
            raise StopIteration
        result = self._next_element
        self._prime()
        return result


    def _prime(self):
        try:
            self._next_element = next(self._myiter)
            self._has_next = 1
        except StopIteration:
            self.next_element = None
            self._has_next = 0


def _test():
    cmp = lambda x,y : x-y
    try:
        for item in mergeiterator(iter([2, 4, 6, 8]), iter([1, 3, 4, 7, 9, 10]), cmp):
           print (item)
    except:
        pass
    
if __name__ == '__main__':
      _test()
