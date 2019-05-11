from hackernewslib.models import Story, Comment, Job, Poll, Part, Ask, Item


class Loader(object):
    def __init__(self):
        self.supported_item_types = [Story, Comment, Job, Poll, Part, Ask]

    def load(self, client, data):
        item_id = data["id"]
        item_type = data.get("type")

        for supported_item_type in self.supported_item_types:
            if supported_item_type.item_type == item_type:
                return supported_item_type.parse(
                    client=client,
                    item=data
                )

        return Item(
            client=client,
            id=item_id,
            data=data
        )
