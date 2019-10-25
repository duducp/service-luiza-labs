from flask_restplus import Resource

from app.handlers.client_handler import ClientHandler
from app.restplus import api
from app.schemas.routes.client_schema import ClientSchemaRoute

ns = api.namespace(
    path="/clients", name="Clients", description="CRUD of the Clients."
)

schema = ClientSchemaRoute()

parser_id = api.parser()
parser_id.add_argument(
    "_id",
    type=str,
    help="Client identifier of type UUID",
    location="path",
    required=True,
)

pagination = api.parser()
pagination.add_argument(
    "page",
    type=int,
    help="Page searching the data",
    location="args",
    default=1,
    required=False,
)
pagination.add_argument(
    "limit",
    type=int,
    help="Number of records to be returned per search",
    location="args",
    default=10,
    required=False,
)


@ns.route("/<_id>")
@api.expect(parser_id)
@api.response(code=400, description="bad_request")
@api.response(code=404, description="not_found")
@api.response(code=500, description="internal_error")
class ClientItem(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = ClientHandler()

    @api.response(code=200, model=schema.response_client, description="success")
    @api.doc(security=True)
    def get(self, _id):
        """
        Returns one registered client
        """
        return self.handler.get_one(_id)

    @api.response(code=200, model=schema.response_client, description="success")
    @api.doc(security=True, body=schema.client_item)
    def put(self, _id):
        """
        Update one client and all required fields must be entered
        """
        return self.handler.put_patch(_id=_id, partial=False)

    @api.response(code=200, description="success")
    @api.doc(security=True, body=schema.client_item)
    def patch(self, _id):
        """
        Update one client and you do not need to enter all fields
        """
        return self.handler.put_patch(_id=_id, partial=True)

    @api.response(code=204, description="success")
    @api.doc(security=True)
    def delete(self, _id):
        """
        Delete one client
        """
        return self.handler.delete(_id=_id)


@ns.route("")
@api.response(code=400, description="bad_request")
@api.response(code=404, description="not_found")
@api.response(code=500, description="internal_error")
class ClientCollection(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = ClientHandler()

    @api.response(code=200, model=schema.response_pagination_client, description="success")
    @api.doc(security=True, parser=pagination)
    def get(self):
        """
        Returns registered clients
        """
        return self.handler.get_all()

    @api.response(code=201, model=schema.response_client, description="success")
    @api.doc(security=True, body=schema.client_item)
    def post(self):
        """
        Create one client
        """
        return self.handler.post()
