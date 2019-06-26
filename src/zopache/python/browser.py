# -*- coding: utf-8 -*-


class FileRenderer(object):

    def __init__(self, rfile):
        self.iterator = rfile

    def __iter__(self):
        return iter(self.rfile)

    @classmethod
    def make_response(cls, rfile, response_factory):
        fileobj = cls(rfile)
        res = response_factory(content_type=rfile.mime)
        res.content_disposition = 'attachment; filename="%s"' % rfile.name
        res.app_iter = fileobj
        res.content_length = rfile.size
        return res
