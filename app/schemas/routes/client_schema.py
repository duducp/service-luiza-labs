from flask_restplus import fields
from app.restplus import api

from app.schemas.routes import response_serializer


class ClientSchemaRoute:
    def __init__(self):
        self._name = "Client"

    @property
    def client_item(self):
        """
        Serializer do cliente
        """
        return api.model(
            f"{self._name}",
            {
                "id": fields.String(readonly=True),
                "name": fields.String(required=True),
                "email": fields.String(required=True),
            },
        )

    @property
    def response_client(self):
        """
        Serializer de resposta do cliente
        """
        return response_serializer(
            data=self.client_item, name_model=f"{self._name}Response"
        )

    @property
    def response_pagination_client(self):
        """
        Serializer de resposta com paginação do cliente
        """
        return response_serializer(
            data=self.client_item,
            name_model=f"{self._name}ResponsePagination",
            name_model_pagination=f"{self._name}Pagination",
            pagination=True,
        )
