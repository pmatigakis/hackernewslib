class Item(object):
    def __init__(self, client, id, deleted=None, type=None, by=None, time=None,
                 text=None, dead=None, parent=None, poll=None, kids=None,
                 url=None, score=None, title=None, parts=None,
                 descendants=None):
            self.client = client
            self.id = id
            self.deleted = deleted
            self.type = type
            self.by = by
            self.time = time
            self.text = text
            self.dead = dead
            self._parent = parent
            self._poll = poll
            self._kids = kids
            self.url = url
            self.score = score
            self.title = title
            self._parts = parts
            self.descendants = descendants

    @property
    def parent(self):
        return (
            self.client.item(self._parent)
            if self._parent is not None
            else None
        )

    @property
    def poll(self):
        return (
            self.client.item(self._poll)
            if self._poll is not None
            else None
        )

    @property
    def kids(self):
        kid_ids = self._kids or []

        return self.client.items(kid_ids)

    @property
    def parts(self):
        part_ids = self._parts or []

        return self.client.items(part_ids)
