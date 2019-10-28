from flask import request, session
from logzero import logger

from app import db
from app.controllers.favorite_controller import FavoriteController
from app.models.favorite_model import FavoriteModel
from app.schemas.models.favorite_schema import FavoriteSchema
from app.services.products_service import ProductService
from app.utils.format_response import Response


class FavoriteHandler:
    def __init__(self):
        self._controller = FavoriteController()
        self._response = Response()
        self._product_service = ProductService()

    def get_all_by_client(self, client_id: str):
        args = request.args.to_dict()
        return self._controller.get_all_by_client(args=args, client_id=client_id)

    def get_all_by_client_details_product(self, client_id: str):
        args = request.args.to_dict()
        return self._controller.get_all_by_client_details_product(
            args=args, client_id=client_id
        )

    def delete(self, _id: str, client_id: str):
        favorite = (
            db.session.query(FavoriteModel)
            .filter(FavoriteModel.id == _id)
            .filter(FavoriteModel.client_id == client_id)
            .first()
        )
        if not favorite:
            return self._response.send(
                status=404,
                message="Favorite ID you entered could not be found",
                code="favorite_not_found",
            )

        return self._controller.delete(_id=_id, client_id=client_id)

    def post(self, client_id: str):
        body = request.get_json(silent=True, force=True)
        body["client_id"] = client_id

        data, errors = FavoriteSchema().load(data=body)
        if errors:
            return self._response.send(
                data=errors,
                status=400,
                message="The body does not match the scheme",
                code="body_incorrect",
            )

        try:
            product = self._product_service.get_one(_id=data.product_id)
            if product.status_code == 404:
                return self._response.send(
                    status=404,
                    message="The product entered was not found",
                    code="product_not_found",
                )
            elif product.status_code != 200:
                logger.error(
                    f"Status code returned when fetching the product was {product.status_code}: {product.text}"
                )
                raise Exception("Failed to register favorite product")
        except Exception as e:
            logger.error(str(e))
            return self._response.send(
                status=500, message=str(e), code="internal_error"
            )

        return self._controller.post(data=data)
