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
        return api.model(f"{self._name}", {
            "id": fields.String(readonly=True),
            "product_id": fields.String(required=True),
        })

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
