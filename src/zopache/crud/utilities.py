def title_or_name(obj):
    title = getattr(obj, 'title', None)
    if title is not None:
        return title
    return getattr(obj, '__name__', u'')
