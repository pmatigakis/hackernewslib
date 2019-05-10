from hackernewslib.models import Story, Raw, Comment, Job, Poll, Part, Ask


class Loader(object):
    def __init__(self):
        self.item_mapper = {
            "story": (
                ["by", "descendants", "kids", "score", "time", "title", "url"],
                Story
            ),
            "comment": (
                ["by", "kids", "parent", "text", "time"],
                Comment
            ),
            "ask": (
                ["by", "descendants", "kids", "score", "text", "time", "title",
                 "url"],
                Ask
            ),
            "job": (
                ["by", "score", "text", "time", "title", "url"],
                Job
            ),
            "poll": (
                ["by", "descendants", "kids", "parts", "score", "text", "time",
                 "title"],
                Poll
            ),
            "part": (
                ["by", "poll", "score", "text", "time"],
                Part
            )
        }

    def load(self, client, data):
        item_loader = self.item_mapper.get(data["type"])
        item_id = data["id"]

        if item_loader is None:
            return Raw(
                client=client,
                id=item_id,
                data=data
            )

        required_fields, klass = item_loader
        return klass(
            client=client,
            id=item_id,
            **{field: data[field] for field in required_fields if field in data}
        )
