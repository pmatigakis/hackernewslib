from firebase.firebase import FirebaseApplication

from hackernewslib.schemas import ItemSchema


def create_client(api_url="https://hacker-news.firebaseio.com"):
    app = FirebaseApplication(api_url, None)

    return HackernewsFirebaseClient(app)


class HackernewsFirebaseClient(object):
    def __init__(self, app):
        self.app = app

        self.item_schema = ItemSchema()

    @property
    def api_url(self):
        return self.app.dsn

    def max_item(self):
        return self.app.get("/v0//maxitem", None)

    def item(self, item_id):
        item_data = self.app.get("/v0//item", item_id)
        deserialization_result = self.item_schema.load(item_data)

        return deserialization_result.data

    def items(self, item_ids):
        for item_id in item_ids:
            item = self.item(item_id)

            yield item

    def user(self, username):
        return self.app.get("/v0//user", username)

    def _group_story_ids(self, story_group):
        return self.app.get(story_group, None)

    def _group_stories(self, story_group, max_stories=None):
        story_ids = self._group_story_ids("/v0/{}".format(story_group))
        if max_stories:
            story_ids = story_ids[:max_stories]

        return self.items(story_ids)

    def new(self, max_stories=None):
        return self._group_stories(
            story_group="newstories",
            max_stories=max_stories
        )

    def top(self, max_stories=None):
        return self._group_stories(
            story_group="topstories",
            max_stories=max_stories
        )

    def best(self, max_stories=None):
        return self._group_stories(
            story_group="beststories",
            max_stories=max_stories
        )

    def ask(self, max_stories=None):
        return self._group_stories(
            story_group="askstories",
            max_stories=max_stories
        )

    def show(self, max_stories=None):
        return self._group_stories(
            story_group="showstories",
            max_stories=max_stories
        )

    def job(self, max_stories=None):
        return self._group_stories(
            story_group="jobstories",
            max_stories=max_stories
        )

    def updates(self):
        return self.app.get("/v0//updates", None)
