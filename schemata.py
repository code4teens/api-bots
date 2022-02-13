from marshmallow import fields, post_load, Schema

from models import Bot


class BotSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()
    user_id = fields.Integer(load_only=True)
    cohort_id = fields.Integer(load_only=True)
    msg_id = fields.Integer()
    created_at = fields.DateTime(dump_only=True)
    last_updated = fields.DateTime(dump_only=True)

    user = fields.Nested('UserSchema', dump_only=True)
    cohort = fields.Nested('CohortSchema', dump_only=True)

    @post_load
    def make_bot(self, data, **kwargs):
        return Bot(**data)


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()


class CohortSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    nickname = fields.String()
