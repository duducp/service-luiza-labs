from app import db

import settings
from app.models.client_model import ClientModel
from app.utils.format_response import Response
from app.utils.jwt import JwtUtils


class AuthController:
    def __init__(self):
        self._config = settings.load_config()
        self._response = Response()
        self._jwt = JwtUtils()

    def login(self, email: str):
        try:
            data = (
                db.session.query(ClientModel).filter(ClientModel.email == email).first()
            )
            if not data:
                return self._response.send(
                    message="Login data is invalid",
                    code="invalid_credentials",
                    status=403,
                )

            data = self._jwt.generate_access_and_refresh_token(client_id=data.id)

            return self._response.send(
                data=data, message="Token created", code="success", status=201
            )
        except Exception as e:
            raise e

    def refresh(self, token: str):
        payload = self._jwt.valid_token(token=token)
        if not payload:
            return self._response.send(
                message="The token entered has expired",
                code="token_expired",
                status=401,
            )

        self._jwt.revoke(
            key=payload.get("jti_access"),
            expires_minutes=self._config.TOKEN_ACCESS_EXP_MINUTES,
        )

        self._jwt.revoke(
            key=payload.get("jti_refresh"),
            expires_minutes=self._config.TOKEN_REFRESH_EXP_MINUTES,
        )

        data = self._jwt.generate_access_and_refresh_token(
            client_id=payload.get("client_id")
        )

        return self._response.send(
            data=data, message="Rebuilt token", code="success", status=201
        )

    def valid(self, token: str):
        is_validated = self._jwt.valid_token(token=token)
        if not is_validated:
            return self._response.send(
                message="The token entered has expired",
                code="token_expired",
                status=401,
            )

        return self._response.send(message="Valid token", code="success", status=204)

    def logout(self, token: str):
        payload = self._jwt.valid_token(token=token)

        if payload:
            self._jwt.revoke(
                key=payload.get("jti_access"),
                expires_minutes=self._config.TOKEN_ACCESS_EXP_MINUTES,
            )

            self._jwt.revoke(
                key=payload.get("jti_refresh"),
                expires_minutes=self._config.TOKEN_REFRESH_EXP_MINUTES,
            )

        return self._response.send(message="Logout done", code="success", status=204)
