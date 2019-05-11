from hackernewslib.models import Story, Comment, Job, Poll, Part, Ask, Item


class Loader(object):
    def __init__(self):
        self.supported_item_types = {
            "story": Story,
            "comment": Comment,
            "job": Job,
            "poll": Poll,
            "part": Part,
            "ask": Ask
        }

    def load(self, client, data):
        item_id = data["id"]

        item_class = self.supported_item_types.get(data.get("type"))
        if item_class is None:
            return Item(
                client=client,
                id=item_id,
                data=data
            )

        return item_class.parse(
            client=client,
            item=data
        )
