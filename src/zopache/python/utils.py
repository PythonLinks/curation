# -*- coding: utf-8 -*-

import os
from . import FSError, ChRootError

RXW = (os.F_OK,
       os.R_OK,
       os.W_OK,
       os.X_OK)


def access_permissions(path, *perms):
    for perm in perms:
        if not os.access(path, os.W_OK):
            return False
    return True


def assert_directory_access(path, mkdir=False):
    if not os.path.exists(path):
        if mkdir is True:
            os.makedirs(path, 0o755)
            return True
        else:
            raise FSError('Folder %r does not exist.' % path)
    if not os.path.isdir(path):
        raise FSError('%r exists and is not a folder' % path)
    else:
        assert access_permissions(path, *RXW)
    return True


def create_directory(path, chroot=None):
    """Returns True if the creation was complete or if
    the folder already exists and is writeable.
    """
    realpath = os.path.realpath(path)
    if chroot is not None:
        rooted = os.path.realpath(chroot)
        if not os.path.isdir(rooted):
            raise ChRootError('%r is not a valid directory.' % chroot)
        if not realpath.startswith(rooted):
            raise ChRootError('%r is not contained in the root %r.' % 
                              (path, chroot))
        assert access_permissions(rooted, *RXW)

    return assert_directory_access(realpath, mkdir=True)
