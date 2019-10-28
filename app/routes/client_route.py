from flask_restplus import Resource

from app.decorators.auth import valid_token
from app.handlers.client_handler import ClientHandler
from app.handlers.favorite_handler import FavoriteHandler
from app.restplus import api
from app.schemas.routes.client_schema import ClientSchemaRoute
from app.schemas.routes.favorite_schema import FavoritesSchemaRoute

ns = api.namespace(path="/clients", name="Clients", description="Gerencia os cliente e seus favoritos no sistema")

schema = ClientSchemaRoute()
schema_favorite = FavoritesSchemaRoute()

parser_client_favorite_id = api.parser()
parser_client_favorite_id.add_argument(
    "client_id",
    type=str,
    help="Client identifier of type UUID",
    location="path",
    required=True,
)
parser_client_favorite_id.add_argument(
    "favorite_id",
    type=str,
    help="Favorite identifier of type UUID",
    location="path",
    required=True,
)

parser_client_id = api.parser()
parser_client_id.add_argument(
    "client_id",
    type=str,
    help="Client identifier of type UUID",
    location="path",
    required=True,
)

parser_favorite_id = api.parser()
parser_favorite_id.add_argument(
    "favorite_id",
    type=str,
    help="Favorite identifier of type UUID",
    location="path",
    required=True,
)

pagination_client = api.parser()
pagination_client.add_argument(
    "page",
    type=int,
    help="Page searching the data",
    location="args",
    default=1,
    required=False,
)
pagination_client.add_argument(
    "limit",
    type=int,
    help="Number of records to be returned per search",
    location="args",
    default=10,
    required=False,
)


@ns.route("/<client_id>")
@api.expect(parser_client_id)
@api.response(code=400, description="bad_request")
@api.response(code=404, description="not_found")
@api.response(code=500, description="internal_error")
class ClientItem(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = ClientHandler()

    @api.response(code=200, model=schema.response_client, description="success")
    @api.doc(security=True)
    @valid_token
    def get(self, client_id):
        """
        Retorna os dados de um determinado cliente
        """
        return self.handler.get_one(client_id)

    @api.response(code=200, model=schema.response_client, description="success")
    @api.doc(security=True, body=schema.client_item)
    @valid_token
    def put(self, client_id):
        """
        Atualiza um cliente onde é nescessário informar todos os campos obrigatórios
        """
        return self.handler.put_patch(_id=client_id, partial=False)

    @api.response(code=200, description="success")
    @api.doc(security=True, body=schema.client_item)
    @valid_token
    def patch(self, client_id):
        """
        Atualiza um cliente onde não é nescessário inserir todos os campos
        """
        return self.handler.put_patch(_id=client_id, partial=True)

    @api.response(code=204, description="success")
    @api.doc(security=True)
    @valid_token
    def delete(self, client_id):
        """
        Exclui de cliente
        """
        return self.handler.delete(_id=client_id)


@ns.route("")
@api.response(code=400, description="bad_request")
@api.response(code=404, description="not_found")
@api.response(code=500, description="internal_error")
class ClientCollection(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = ClientHandler()

    @api.response(
        code=200, model=schema.response_pagination_client, description="success"
    )
    @api.doc(security=True, parser=pagination_client)
    @valid_token
    def get(self):
        """
        Retorna todos os clientes cadastrados
        """
        return self.handler.get_all()

    @api.response(code=201, model=schema.response_client, description="success")
    @api.doc(security=True, body=schema.client_item)
    @valid_token
    def post(self):
        """
        Cadastra um cliente
        """
        return self.handler.post()


@ns.route("/<client_id>/favorites")
@api.expect(parser_client_id)
@api.response(code=400, description="bad_request")
@api.response(code=404, description="not_found")
@api.response(code=500, description="internal_error")
class ClientIdFavorite(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = FavoriteHandler()

    @api.response(
        code=200,
        model=schema_favorite.response_pagination_favorite,
        description="success",
    )
    @api.doc(security=True, parser=pagination_client)
    @valid_token
    def get(self, client_id):
        """
        Busca todos favoritos do cliente logado
        """
        return self.handler.get_all_by_client(client_id=client_id)

    @api.response(
        code=201, model=schema_favorite.response_favorite, description="success"
    )
    @api.doc(security=True, body=schema_favorite.favorite_item)
    @valid_token
    def post(self, client_id):
        """
        Cadastra um produto aos favoritos do cliente logado
        """
        return self.handler.post(client_id=client_id)


@ns.route("/<client_id>/favorites/details")
@api.expect(parser_client_id)
@api.response(code=400, description="bad_request")
@api.response(code=404, description="not_found")
@api.response(code=500, description="internal_error")
class ClientIdFavoriteDetails(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = FavoriteHandler()

    @api.response(
        code=200,
        model=schema_favorite.response_pagination_favorite_details,
        description="success",
    )
    @api.doc(security=True, parser=pagination_client)
    @valid_token
    def get(self, client_id):
        """
        Busca todos favoritos do cliente logado e os detalhes de cada produto
        """
        return self.handler.get_all_by_client_details_product(client_id=client_id)


@ns.route("/<client_id>/favorites/<favorite_id>")
@api.expect(parser_client_favorite_id)
@api.expect(parser_favorite_id)
@api.response(code=400, description="bad_request")
@api.response(code=404, description="not_found")
@api.response(code=500, description="internal_error")
class ClientIdFavoriteId(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = FavoriteHandler()

    @api.response(code=204, description="success")
    @api.doc(security=True)
    @valid_token
    def delete(self, client_id, favorite_id):
        """
        Exclui um favorito do cliente logado
        """
        return self.handler.delete(_id=favorite_id, client_id=client_id)
