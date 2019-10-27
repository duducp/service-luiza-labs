from flask_restplus import Resource

from app.handlers.auth_handler import AuthHandler
from app.handlers.client_handler import ClientHandler
from app.restplus import api
from app.schemas.routes.auth_schema import AuthSchemaRoute
from app.schemas.routes.client_schema import ClientSchemaRoute

ns = api.namespace(
    path="/auth",
    name="Auth",
    description="Gerencia a parte de autorização do acesso ao sistema",
)

schema = AuthSchemaRoute()
schema_client = ClientSchemaRoute()


@ns.route("/login")
@api.doc(security=None)
@api.response(code=500, description="internal_error")
@api.response(code=401, description="unauthorized")
class Login(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = AuthHandler()

    @api.response(code=201, model=schema.auth_response_final, description="success")
    @api.expect(schema.auth_request)
    def post(self):
        """
        Realiza o login do cliente no sistema
        """
        return self.handler.login()


@ns.route("/register")
@api.doc(security=None)
@api.response(code=500, description="internal_error")
@api.response(code=401, description="unauthorized")
class Register(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = ClientHandler()

    @api.response(code=201, model=schema_client.response_client, description="success")
    @api.doc(security=False, body=schema_client.client_item)
    def post(self):
        """
        Cadastra um novo cliente no sistema para o mesmo poder fazer o login posteriormente
        """
        return self.handler.post()


@ns.route("/logout")
@api.doc(security=None)
@api.response(code=500, description="internal_error")
class Logout(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = AuthHandler()

    @api.response(code=204, description="success")
    @api.doc(security=["authorization"])
    def get(self):
        """
        Inválida os tokens do cliente quando o mesmo fazer logout no sistema
        """
        return self.handler.logout()


@ns.route("/refresh")
@api.doc(security=None)
@api.response(code=500, description="internal_error")
@api.response(code=401, description="unauthorized")
class Refresh(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = AuthHandler()

    @api.response(code=201, model=schema.auth_response_final, description="success")
    @api.doc(security=["authorization"])
    def get(self):
        """
        Renova o token do cliente
        """
        return self.handler.refresh()


@ns.route("/valid")
@api.doc(security=None)
@api.response(code=500, description="internal_error")
@api.response(code=401, description="unauthorized")
class ValidToken(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = AuthHandler()

    @api.response(code=204, description="success")
    @api.doc(security=["authorization"])
    def get(self):
        """
        Verifica se o token é válido
        """
        return self.handler.valid()
