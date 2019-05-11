from unittest import TestCase, main
from unittest.mock import MagicMock

from hackernewslib.clients import HackernewsFirebaseClient
from hackernewslib.exceptions import InvalidItemContents
from hackernewslib.models import Story, Comment, Job, Poll, Part, Item, User


class HackernewsFirebaseClientTests(TestCase):
    def test_get_story(self):
        firebase_app = MagicMock()
        firebase_app.get.return_value = {
            "by": "user_1",
            "descendants": 10,
            "id": 1,
            "kids": [2, 3],
            "score": 100,
            "time": 1175714200,
            "title": "This is a story",
            "type": "story",
            "url": "http://www.example.com/story_1"
        }

        client = HackernewsFirebaseClient(firebase_app)
        story = client.item(1)

        self.assertIsInstance(story, Story)
        self.assertEqual(story.id, 1)
        self.assertEqual(story.descendants, 10)
        self.assertEqual(story.by_username, "user_1")
        self.assertCountEqual(story.kid_ids, [2, 3])
        self.assertEqual(story.score, 100)
        self.assertEqual(story.time, 1175714200)
        self.assertEqual(story.title, "This is a story")
        self.assertEqual(story.type, "story")
        self.assertEqual(story.url, "http://www.example.com/story_1")
        self.assertIsNone(story.text)

        firebase_app.get.assert_called_once_with("/v0//item", 1)

    def test_get_comment(self):
        firebase_app = MagicMock()
        firebase_app.get.return_value = {
            "by": "user_1",
            "id": 1,
            "kids": [2, 3],
            "parent": 4,
            "text": "This is a comment",
            "time": 1314211127,
            "type": "comment"
        }

        client = HackernewsFirebaseClient(firebase_app)
        comment = client.item(1)

        self.assertIsInstance(comment, Comment)
        self.assertEqual(comment.id, 1)
        self.assertEqual(comment.parent_id, 4)
        self.assertEqual(comment.by_username, "user_1")
        self.assertCountEqual(comment.kid_ids, [2, 3])
        self.assertEqual(comment.text, "This is a comment")
        self.assertEqual(comment.type, "comment")
        self.assertEqual(comment.time, 1314211127)

        firebase_app.get.assert_called_once_with("/v0//item", 1)

    def test_get_ask(self):
        firebase_app = MagicMock()
        firebase_app.get.return_value = {
            "by": "user_1",
            "descendants": 10,
            "id": 1,
            "kids": [2, 3],
            "score": 100,
            "text": "This is the question text",
            "time": 1203647620,
            "title": "This is a question",
            "type": "story",
            "url": "http://www.example.com/question_1"
        }

        client = HackernewsFirebaseClient(firebase_app)
        story = client.item(1)

        self.assertIsInstance(story, Story)
        self.assertEqual(story.id, 1)
        self.assertEqual(story.descendants, 10)
        self.assertEqual(story.by_username, "user_1")
        self.assertCountEqual(story.kid_ids, [2, 3])
        self.assertEqual(story.score, 100)
        self.assertEqual(story.time, 1203647620)
        self.assertEqual(story.title, "This is a question")
        self.assertEqual(story.type, "story")
        self.assertEqual(story.url, "http://www.example.com/question_1")
        self.assertEqual(story.text, "This is the question text")

        firebase_app.get.assert_called_once_with("/v0//item", 1)

    def test_get_job(self):
        firebase_app = MagicMock()
        firebase_app.get.return_value = {
            "by": "user_1",
            "id": 1,
            "score": 100,
            "text": "This is a job post",
            "time": 1210981217,
            "title": "Job post",
            "type": "job",
            "url": "http://www.example.com/job_1"
        }

        client = HackernewsFirebaseClient(firebase_app)
        job = client.item(1)

        self.assertIsInstance(job, Job)
        self.assertEqual(job.id, 1)
        self.assertEqual(job.by_username, "user_1")
        self.assertEqual(job.score, 100)
        self.assertEqual(job.time, 1210981217)
        self.assertEqual(job.title, "Job post")
        self.assertEqual(job.type, "job")
        self.assertEqual(job.url, "http://www.example.com/job_1")
        self.assertEqual(job.text, "This is a job post")

        firebase_app.get.assert_called_once_with("/v0//item", 1)

    def test_get_poll(self):
        firebase_app = MagicMock()
        firebase_app.get.return_value = {
            "by": "user_1",
            "descendants": 10,
            "id": 1,
            "kids": [2, 3],
            "parts": [4, 5, 6],
            "score": 100,
            "text": "This is the poll text",
            "time": 1204403652,
            "title": "This is a poll",
            "type": "poll"
        }

        client = HackernewsFirebaseClient(firebase_app)
        poll = client.item(1)

        self.assertIsInstance(poll, Poll)
        self.assertEqual(poll.id, 1)
        self.assertEqual(poll.by_username, "user_1")
        self.assertEqual(poll.descendants, 10)
        self.assertEqual(poll.score, 100)
        self.assertEqual(poll.time, 1204403652)
        self.assertEqual(poll.title, "This is a poll")
        self.assertEqual(poll.type, "poll")
        self.assertEqual(poll.text, "This is the poll text")
        self.assertCountEqual(poll.kid_ids, [2, 3])
        self.assertCountEqual(poll.part_ids, [4, 5, 6])

        firebase_app.get.assert_called_once_with("/v0//item", 1)

    def test_get_part(self):
        firebase_app = MagicMock()
        firebase_app.get.return_value = {
            "by": "user_1",
            "id": 1,
            "poll": 2,
            "score": 100,
            "text": "This is the part text",
            "time": 1207886576,
            "type": "pollopt"
        }

        client = HackernewsFirebaseClient(firebase_app)
        poll = client.item(1)

        self.assertIsInstance(poll, Part)
        self.assertEqual(poll.id, 1)
        self.assertEqual(poll.by_username, "user_1")
        self.assertEqual(poll.score, 100)
        self.assertEqual(poll.time, 1207886576)
        self.assertEqual(poll.type, "pollopt")
        self.assertEqual(poll.text, "This is the part text")
        self.assertEqual(poll.poll_id, 2)

        firebase_app.get.assert_called_once_with("/v0//item", 1)

    def test_get_unknown_item(self):
        firebase_app = MagicMock()
        firebase_app.get.return_value = None

        client = HackernewsFirebaseClient(firebase_app)
        item = client.item(1)

        self.assertIsNone(item)

        firebase_app.get.assert_called_once_with("/v0//item", 1)

    def test_get_unknown_item_type(self):
        firebase_app = MagicMock()
        firebase_app.get.return_value = {
            "id": 1,
            "type": "unknown",
            "message": "hello"
        }

        client = HackernewsFirebaseClient(firebase_app)
        item = client.item(1)

        self.assertIsInstance(item, Item)
        self.assertEqual(item.id, 1)
        self.assertEqual(item.type, "unknown")
        self.assertDictEqual(
            item.data,
            {
                "id": 1,
                "type": "unknown"
            }
        )

        firebase_app.get.assert_called_once_with("/v0//item", 1)

    def test_get_malformed_item(self):
        firebase_app = MagicMock()
        firebase_app.get.return_value = {
            "message": "hello"
        }

        client = HackernewsFirebaseClient(firebase_app)

        with self.assertRaises(InvalidItemContents) as e:
            client.item(1)

        self.assertDictEqual(
            e.exception.data,
            {
                "message": "hello"
            }
        )

        self.assertDictEqual(
            e.exception.errors,
            {
                "id": ["Missing data for required field."]
            }
        )

        firebase_app.get.assert_called_once_with("/v0//item", 1)

    def test_get_user(self):
        firebase_app = MagicMock()
        firebase_app.get.return_value = {
            "about": "This is a user",
            "created": 1173923446,
            "delay": 0,
            "id": "user_1",
            "karma": 100,
            "submitted": [1, 2, 3]
        }

        client = HackernewsFirebaseClient(firebase_app)
        user = client.user("user_1")

        self.assertIsInstance(user, User)
        self.assertEqual(user.id, "user_1")
        self.assertEqual(user.created, 1173923446)
        self.assertEqual(user.delay, 0)
        self.assertEqual(user.about, "This is a user")
        self.assertEqual(user.karma, 100)
        self.assertCountEqual(user.submitted_ids, [1, 2, 3])

        firebase_app.get.assert_called_once_with("/v0//user", "user_1")

    def test_get_user_that_does_not_exist(self):
        firebase_app = MagicMock()
        firebase_app.get.return_value = None

        client = HackernewsFirebaseClient(firebase_app)
        user = client.user("user_1")

        self.assertIsNone(user)

        firebase_app.get.assert_called_once_with("/v0//user", "user_1")

    def test_get_user_with_malformed_response(self):
        firebase_app = MagicMock()
        firebase_app.get.return_value = {
            "message": "hello"
        }

        client = HackernewsFirebaseClient(firebase_app)

        with self.assertRaises(InvalidItemContents) as e:
            client.user("user_1")

        self.assertDictEqual(
            e.exception.data,
            {
                "message": "hello"
            }
        )

        self.assertDictEqual(
            e.exception.errors,
            {
                "created": ["Missing data for required field."],
                "id": ["Missing data for required field."],
                "karma": ["Missing data for required field."]
            }
        )

        firebase_app.get.assert_called_once_with("/v0//user", "user_1")


if __name__ == "__main__":
    main()
