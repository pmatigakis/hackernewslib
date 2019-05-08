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
            self.parent_id = parent
            self._parent = None
            self.poll_id = poll
            self._poll = None
            self.kid_ids = kids
            self._kids = None
            self.url = url
            self.score = score
            self.title = title
            self.part_ids = parts
            self._parts = None
            self.descendants = descendants

    @property
    def parent(self):
        if self.parent_id is not None and self._parent is None:
            self._parent = self.client.item(self.parent_id)

        return self._parent

    @property
    def poll(self):
        if self.poll_id is not None and self._poll is None:
            self._poll = self.client.item(self.poll_id)

        return self._poll

    @property
    def kids(self):
        if self._kids is not None:
            for kid in self._kids:
                yield kid
        else:
            kid_ids = self.kid_ids or []
            self._kids = []

            for kid in self.client.items(kid_ids):
                self._kids.append(kid)
                yield kid

    @property
    def parts(self):
        if self._parts is not None:
            for part in self._parts:
                yield part
        else:
            part_ids = self.part_ids or []
            self._parts = []

            for part in self.client.items(part_ids):
                self._parts.append(part)
                yield part
