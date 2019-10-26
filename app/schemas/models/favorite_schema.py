from marshmallow import fields

from app.marshmallow import ma
from app.models.favorite_model import FavoriteModel


class FavoriteSchema(ma.ModelSchema):
    class Meta:
        model = FavoriteModel

    id = fields.UUID(dump_only=True)
    client_id = fields.UUID(required=True)
    product_id = fields.UUID(required=True)


class FavoriteProductSchema(ma.ModelSchema):
    class Meta:
        model = FavoriteModel

    id = fields.UUID(dump_only=True)
    client_id = fields.UUID(required=True)
    product_id = fields.UUID(required=True)
    product = fields.Nested("ProductSchema", many=False)


class ProductSchema(ma.ModelSchema):
    price = fields.Number(dump_only=True)
    reviewScore = fields.Number(dump_only=True, default=0)
    image = fields.String(dump_only=True)
    title = fields.String(dump_only=True)
    brand = fields.String(dump_only=True)
    id = fields.String(dump_only=True)
