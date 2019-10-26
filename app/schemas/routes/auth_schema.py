from flask_restplus import fields
from app.restplus import api

from app.schemas.routes import response_serializer


class AuthSchemaRoute:
    def __init__(self):
        self._name = "Auth"

    @property
    def auth_response(self):
        """
        Serializer de Response do Auth
        """
        return api.model(
            f"{self._name}Response",
            {
                "access_token": fields.String(readonly=True),
                "refresh_token": fields.String(readonly=True),
            },
        )

    @property
    def auth_response_final(self):
        """
        Serializer de Response do Auth formatado
        """
        return response_serializer(
            data=self.auth_response, name_model=f"{self._name}ResponseFinal"
        )

    @property
    def auth_request(self):
        """
        Serializer de Request do Auth
        """
        return api.model(f"{self._name}Request", {"email": fields.String(require=True)})
