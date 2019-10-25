from marshmallow import fields, validate
from marshmallow.validate import Email

from app.marshmallow import ma
from app.models.client_model import ClientModel


class ClientSchema(ma.ModelSchema):
    class Meta:
        model = ClientModel

    id = fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=5))
    email = fields.Email(required=True, validate=Email)
