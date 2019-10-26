from flask_restplus import Resource

from app.handlers.auth_handler import AuthHandler
from app.restplus import api
from app.schemas.routes.auth_schema import AuthSchemaRoute

ns = api.namespace(
    path="/auth",
    name="Auth",
    description="Manages the authorization part of system access",
)

schema = AuthSchemaRoute()


@ns.route("/login")
@api.doc(security=None)
@api.response(code=500, description="internal_error")
@api.response(code=401, description="unauthorized")
class Login(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth = AuthHandler()

    @api.response(code=201, model=schema.auth_response_final, description="success")
    @api.expect(schema.auth_request)
    def post(self):
        """
        Log in to the system
        """
        return self.auth.login()


@ns.route("/logout")
@api.doc(security=None)
@api.response(code=500, description="internal_error")
class Logout(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth = AuthHandler()

    @api.response(code=204, description="success")
    @api.doc(security=["authorization"])
    def get(self):
        """
        Log out of the system
        """
        return self.auth.logout()


@ns.route("/refresh")
@api.doc(security=None)
@api.response(code=500, description="internal_error")
@api.response(code=401, description="unauthorized")
class Refresh(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth = AuthHandler()

    @api.response(code=201, model=schema.auth_response_final, description="success")
    @api.doc(security=["authorization"])
    def get(self):
        """
        Renew user token
        """
        return self.auth.refresh()


@ns.route("/valid")
@api.doc(security=None)
@api.response(code=500, description="internal_error")
@api.response(code=401, description="unauthorized")
class ValidToken(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth = AuthHandler()

    @api.response(code=204, description="success")
    @api.doc(security=["authorization"])
    def get(self):
        """
        Checks if the token is valid
        """
        return self.auth.valid()
