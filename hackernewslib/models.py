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
    item_type = None
    fields = []

    def __init__(self, client, id, data):
        self.client = client
        self.id = id
        self.data = data

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
        else:
            setattr(self, field, item.get(field))


class Story(Item, KidsMixin):
    item_type = "story"
    fields = ["by", "descendants", "score", "time", "title", "url", "kids"]


class Comment(Item, KidsMixin):
    item_type = "comment"
    fields = ["by", "text", "time", "kids", "parent"]

    @property
    def parent(self):
        if self.parent_id is not None and self._parent is None:
            self._parent = self.client.item(self.parent_id)

        return self._parent


class Ask(Item, KidsMixin):
    item_type = "ask"
    fields = ["by", "descendants",  "score", "text", "time", "title", "url",
              "kids"]


class Job(Item):
    item_type = "job"
    fields = ["by", "score", "text", "time", "title", "url"]


class Poll(Item, KidsMixin):
    item_type = "poll"
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


class Part(Item):
    item_type = "part"
    fields = ["by", "poll", "score", "text", "time"]

    @property
    def poll(self):
        if self.poll_id is not None and self._poll is None:
            self._poll = self.client.item(self.poll_id)

        return self._poll
