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


class UserMixin(object):
    @property
    def by(self):
        if self.by_username is not None and self._by is None:
            self._by = self.client.user(self.by_username)

        return self._by


class Item(object):
    fields = []

    def __init__(self, client, id, data):
        self.client = client
        self.id = id
        self.data = data
        self.type = data.get("type")

    @classmethod
    def parse(cls, client, item):
        instance = cls(
            client=client,
            id=item["id"],
            data=item
        )

        instance._copy_fields(item, cls.fields)

        return instance

    def _copy_fields(self, item, fields):
        for field in fields:
            self._copy_field(item, field)

    def _copy_field(self, item, field):
        if field == "kids":
            setattr(self, "kid_ids", item.get("kids"))
            setattr(self, "_kids", None)
        elif field == "parent":
            setattr(self, "parent_id", item.get("parent"))
            setattr(self, "_parent", None)
        elif field == "parts":
            setattr(self, "part_ids", item.get("parts"))
            setattr(self, "_parts", None)
        elif field == "poll":
            setattr(self, "poll_id", item.get("poll"))
            setattr(self, "_poll", None)
        elif field == "by":
            setattr(self, "by_username", item.get("by"))
            setattr(self, "_by", None)
        else:
            setattr(self, field, item.get(field))


class Story(Item, KidsMixin, UserMixin):
    fields = ["by", "descendants", "score", "time", "title", "url", "kids",
              "text"]


class Comment(Item, KidsMixin, UserMixin):
    fields = ["by", "text", "time", "kids", "parent"]

    @property
    def parent(self):
        if self.parent_id is not None and self._parent is None:
            self._parent = self.client.item(self.parent_id)

        return self._parent


class Job(Item, UserMixin):
    fields = ["by", "score", "text", "time", "title", "url"]


class Poll(Item, KidsMixin, UserMixin):
    fields = ["by", "descendants", "kids", "parts", "score", "text", "time",
              "title"]

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


class Part(Item, UserMixin):
    fields = ["by", "poll", "score", "text", "time"]

    @property
    def poll(self):
        if self.poll_id is not None and self._poll is None:
            self._poll = self.client.item(self.poll_id)

        return self._poll


class User(object):
    def __init__(self, client, id, created, karma, about=None, delay=None,
                 submitted=None):
        self.client = client
        self.id = id
        self.created = created
        self.karma = karma
        self.about = about
        self.delay = delay
        self.submitted_ids = submitted
        self._submitted = None

    @property
    def submitted(self):
        if self._submitted is not None:
            for item in self._submitted:
                yield item
        else:
            submitted_ids = self.submitted_ids or []
            self._submitted = []

            for item in self.client.items(submitted_ids):
                self._submitted.append(item)
                yield item
