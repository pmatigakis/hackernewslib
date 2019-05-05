class Item(object):
    def __init__(self, id, deleted=None, type=None, by=None, time=None,
                 text=None, dead=None, parent=None, poll=None, kids=None,
                 url=None, score=None, title=None, parts=None,
                 descendants=None):
            self.id = id
            self.deleted = deleted
            self.type = type
            self.by = by
            self.time = time
            self.text = text
            self.dead = dead
            self.parent = parent
            self.poll = poll
            self.kids = kids
            self.url = url
            self.score = score
            self.title = title
            self.parts = parts
            self.descendants = descendants
