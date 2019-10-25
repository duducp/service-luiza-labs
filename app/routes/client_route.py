from flask_restplus import Resource

from app.handlers.client_handler import ClientHandler
from app.restplus import api

ns = api.namespace(
    path="/clients", name="Clients", description="CRUD of the Clients."
)

parser_id = api.parser()
parser_id.add_argument(
    "id",
    type=str,
    help="Client identifier of type UUID",
    location="path",
    required=True,
)


@ns.route("/<id>")
@api.expect(parser_id)
@api.response(code=400, description="bad_request")
@api.response(code=404, description="not_found")
@api.response(code=500, description="internal_error")
class ClientItem(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = ClientHandler()

    @api.response(code=200, description="success")
    @api.doc(security=True, parser=parser_id)
    def get(self, id):
        """
        Returns one registered client
        """
        return self.handler.get_one(id)

    @api.response(code=200, description="success")
    @api.doc(security=True, parser=parser_id)
    def put(self, id):
        """
        Update one client and all required fields must be entered.
        """
        return self.handler.put_patch(_id=id, partial=False)

    @api.response(code=200, description="success")
    @api.doc(security=True)
    def patch(self, id):
        """
        Update one client and you do not need to enter all fields.
        """
        return self.handler.put_patch(_id=id, partial=True)


@ns.route("")
@api.response(code=400, description="bad_request")
@api.response(code=404, description="not_found")
@api.response(code=500, description="internal_error")
class ClientCollection(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = ClientHandler()

    @api.response(code=200, description="success")
    @api.doc(security=True)
    def get(self):
        """
        Returns registered clients
        """
        return self.handler.get_all()

    @api.response(code=201, description="success")
    @api.doc(security=True)
    def post(self):
        """
        Create one client
        """
        return self.handler.post()
