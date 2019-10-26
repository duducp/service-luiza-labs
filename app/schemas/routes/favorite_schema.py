from flask_restplus import fields
from app.restplus import api

from app.schemas.routes import response_serializer


class FavoritesSchemaRoute:
    def __init__(self):
        self._name = "Favorite"

    @property
    def favorite_item(self):
        """
        Serializer dos produtos favoritos dos clientes
        """
        return api.model(
            f"{self._name}",
            {
                "id": fields.String(readonly=True),
                "product_id": fields.String(required=True),
                "client_id": fields.String(readonly=True),
            },
        )

    @property
    def product_item(self):
        """
        Serializer dos produtos
        """
        return api.model(
            "Product",
            {
                "id": fields.String(readonly=True),
                "title": fields.String(readonly=True),
                "reviewScore": fields.Integer(readonly=True),
                "price": fields.Integer(readonly=True),
                "image": fields.String(readonly=True),
                "brand": fields.String(readonly=True),
            },
        )

    @property
    def favorite_product_item(self):
        """
        Serializer dos produtos favoritos dos clientes
        """
        return api.inherit(
            f"{self._name}Product",
            {
                "id": fields.String(readonly=True),
                "product_id": fields.String(required=True),
                "client_id": fields.String(readonly=True),
                "product": fields.Nested(self.product_item),
            },
        )

    @property
    def response_favorite(self):
        """
        Serializer de resposta do produtos favoritos
        """
        return response_serializer(
            data=self.favorite_item, name_model=f"{self._name}Response"
        )

    @property
    def response_pagination_favorite(self):
        """
        Serializer de resposta com paginação dos produtos favoritos
        """
        return response_serializer(
            data=self.favorite_item,
            name_model=f"{self._name}ResponsePagination",
            name_model_pagination=f"{self._name}Pagination",
            pagination=True,
        )

    @property
    def response_pagination_favorite_details(self):
        """
        Serializer de resposta com paginação dos produtos favoritos
        """
        return response_serializer(
            data=self.favorite_product_item,
            name_model=f"{self._name}ProductResponsePagination",
            name_model_pagination=f"{self._name}ProductPagination",
            pagination=True,
        )
