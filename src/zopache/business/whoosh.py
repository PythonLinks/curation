from whoosh.fields import Schema, TEXT, ID, KEYWORD, DATETIME

schema = Schema(
    title=TEXT(field_boost=2.0),
    remoteURL = ID,
    name = ID,
    creationtime =
    keywords= KEYWORD,
    content=TEXT)
