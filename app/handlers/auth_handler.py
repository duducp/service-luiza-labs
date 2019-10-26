from flask import request

from app.controllers.auth_controller import AuthController
from app.schemas.models.auth_schema import AuthSchema
from app.utils.format_response import Response


class AuthHandler:
    def __init__(self):
        self._controller = AuthController()
        self._response = Response()
        self._token = request.headers.get("authorization", None)

    def login(self):
        body = request.get_json(silent=True, force=True)

        data, errors = AuthSchema().load(data=body)
        if errors:
            return self._response.send(
                data=errors,
                status=400,
                message="The body does not match the scheme",
                code="body_incorrect",
            )

        result = self._controller.login(email=body.get("email"))
        return result

    def refresh(self):
        result = self._controller.refresh(self._token)
        return result

    def valid(self):
        result = self._controller.valid(self._token)
        return result

    def logout(self):
        result = self._controller.logout(self._token)
        return result
