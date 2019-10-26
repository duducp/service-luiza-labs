from marshmallow import fields

from app.marshmallow import ma
from app.models.favorite_model import FavoriteModel


class FavoriteSchema(ma.ModelSchema):
    class Meta:
        model = FavoriteModel

    id = fields.UUID(dump_only=True)
    client_id = fields.UUID(required=True)
    product_id = fields.UUID(required=True)
