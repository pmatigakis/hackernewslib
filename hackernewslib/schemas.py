from marshmallow import Schema, fields, post_load

from hackernewslib.models import Item


class ItemSchema(Schema):
    id = fields.Integer(required=True, allow_none=False)
    deleted = fields.Boolean(required=False, allow_none=True)
    type = fields.String(required=False, allow_none=True)
    by = fields.String(required=False, allow_none=True)
    time = fields.Integer(required=False, allow_none=True)
    text = fields.String(required=False, allow_none=True)
    dead = fields.Boolean(required=False, allow_none=True)
    parent = fields.Integer(required=False, allow_none=True)
    poll = fields.Integer(required=False, allow_none=True)
    kids = fields.List(fields.Integer(), required=False, allow_none=True)
    url = fields.Url(required=False, allow_none=True)
    score = fields.Integer(required=False, allow_none=True)
    title = fields.String(required=False, allow_none=True)
    parts = fields.List(fields.Integer(), required=False, allow_none=True)
    descendants = fields.Integer(required=False, allow_none=True)

    @post_load
    def make_item(self, data):
        return Item(**data)
