class KidsMixin(object):
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


class Item(object):
    def __init__(self, client, id):
        self.client = client
        self.id = id


class Story(Item, KidsMixin):
    def __init__(self, client, id, by=None, descendants=None, kids=None,
                 score=None, time=None, title=None, url=None):
        super(Story, self).__init__(
            client=client,
            id=id
        )

        self.by = by
        self.time = time
        self.kid_ids = kids
        self._kids = None
        self.url = url
        self.score = score
        self.title = title
        self.descendants = descendants


class Comment(Item, KidsMixin):
    def __init__(self, client, id, by=None, kids=None, parent=None, text=None,
                 time=None):
        super(Comment, self).__init__(
            client=client,
            id=id
        )

        self.by = by
        self.time = time
        self.text = text
        self.parent_id = parent
        self._parent = None
        self.kid_ids = kids
        self._kids = None

    @property
    def parent(self):
        if self.parent_id is not None and self._parent is None:
            self._parent = self.client.item(self.parent_id)

        return self._parent


class Ask(Item, KidsMixin):
    def __init__(self, client, id, by=None, descendants=None, kids=None,
                 score=None, text=None, time=None, title=None, url=None):
        super(Ask, self).__init__(
            client=client,
            id=id
        )

        self.by = by
        self.time = time
        self.text = text
        self.kid_ids = kids
        self._kids = None
        self.url = url
        self.score = score
        self.title = title
        self.descendants = descendants


class Job(Item):
    def __init__(self, client, id, by=None, score=None, text=None, time=None,
                 title=None, url=None):
        super(Job, self).__init__(
            client=client,
            id=id
        )

        self.by = by
        self.time = time
        self.text = text
        self.url = url
        self.score = score
        self.title = title


class Poll(Item, KidsMixin):
    def __init__(self, client, id, by=None, descendants=None, kids=None,
                 parts=None, score=None, text=None, time=None, title=None):
        super(Poll, self).__init__(
            client=client,
            id=id
        )

        self.by = by
        self.time = time
        self.text = text
        self.kid_ids = kids
        self._kids = None
        self.score = score
        self.title = title
        self.part_ids = parts
        self._parts = None
        self.descendants = descendants

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


class Part(Item):
    def __init__(self, client, id, by=None, poll=None, score=None, text=None,
                 time=None):
        super(Part, self).__init__(
            client=client,
            id=id
        )

        self.by = by
        self.time = time
        self.text = text
        self.poll_id = poll
        self._poll = None
        self.score = score

    @property
    def poll(self):
        if self.poll_id is not None and self._poll is None:
            self._poll = self.client.item(self.poll_id)

        return self._poll


class Raw(Item):
    def __init__(self, client, id, data):
        super(Raw, self).__init__(
            client=client,
            id=id
        )

        self.data = data


class TempItem(object):
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
