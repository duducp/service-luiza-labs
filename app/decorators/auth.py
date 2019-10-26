from functools import wraps

from flask import request, session

from app.controllers.auth_controller import AuthController
from app.utils.format_response import Response
from app.utils.jwt import JwtUtils


def valid_token(f):
    @wraps(f)
    def valid(*args, **kwargs):
        token = request.headers.get("authorization", "")

        if token:
            response = AuthController().valid(token=token)
            if response.status_code != 204:
                return Response().send(
                    message="The token entered is not valid",
                    code="token_invalid",
                    status=401,
                )
            else:
                payload = JwtUtils().decode(token=token, verify=False)
                session["client_id"] = str(payload.get("client_id", None))
        else:
            return Response().send(
                message="The token not entered in header",
                code="token_not_informed",
                status=400,
            )

        return f(*args, **kwargs)

    return valid
