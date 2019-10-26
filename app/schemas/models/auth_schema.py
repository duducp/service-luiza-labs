from flask_marshmallow import Schema
from marshmallow import fields
from marshmallow.validate import Email


class AuthSchema(Schema):
    email = fields.Email(required=True, validate=Email)
