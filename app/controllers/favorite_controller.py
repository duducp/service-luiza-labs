from http import HTTPStatus

from app import db

import settings
from app.models.favorite_model import FavoriteModel
from app.schemas.models.favorite_schema import FavoriteSchema
from app.services.products_service import ProductService
from app.utils.format_response import Response


class FavoriteController:
    def __init__(self):
        self._config = settings.load_config()
        self._response = Response()
        self._product_service = ProductService()

    def get_all_by_client(self, client_id: str, args: dict):
        try:
            query = db.session.query(FavoriteModel).filter(
                FavoriteModel.client_id == client_id
            )
            data = query.paginate(
                page=int(args.get("page", 1)),
                per_page=int(args.get("limit", 10)),
                max_per_page=100,
            )

            return self._response.send(
                schema=FavoriteSchema(many=True),
                status=HTTPStatus.OK,
                data=data,
                code="success",
                message="Favorites found successfully",
            )
        except Exception as e:
            raise e

    def get_all_by_client_details_product(self, client_id: str, args: dict):
        try:
            query = db.session.query(FavoriteModel).filter(
                FavoriteModel.client_id == client_id
            )
            data_pagination = query.paginate(
                page=int(args.get("page", 1)),
                per_page=int(args.get("limit", 10)),
                max_per_page=100,
            )

            data = FavoriteSchema(many=True).dump(data_pagination.items).data
            if data:
                for item in data:
                    product_id = item.get("product_id", "")
                    if product_id:
                        product = self._get_data_product(product_id)
                        item["product"] = product
                    else:
                        item["product"] = {}

            data = {
                "results": data,
                "page": data_pagination.page,
                "size": data_pagination.per_page,
                "total_items": data_pagination.total,
                "total_pages": data_pagination.pages,
            }

            return self._response.send(
                status=HTTPStatus.OK,
                data=data,
                code="success",
                message="Favorites found successfully",
            )
        except Exception as e:
            raise e

    def post(self, data: FavoriteModel):
        try:
            db.session.add(data)
            db.session.commit()

            return self._response.send(
                schema=FavoriteSchema(),
                data=data,
                status=HTTPStatus.CREATED,
                code="success",
                message="Favorite created",
            )
        except Exception as e:
            db.session.rollback()
            raise e
        finally:
            db.session.close()

    def delete(self, _id: str, client_id: str):
        try:
            (
                db.session.query(FavoriteModel)
                .filter(FavoriteModel.id == _id)
                .filter(FavoriteModel.client_id == client_id)
                .delete()
            )
            db.session.commit()

            return self._response.send(
                data=None,
                status=HTTPStatus.NO_CONTENT,
                code="success",
                message="Favorite deleted",
            )
        except Exception as e:
            db.session.rollback()
            raise e
        finally:
            db.session.close()

    def _get_data_product(self, product_id: str) -> dict:
        try:
            product = self._product_service.get_one(product_id)
            if product.status_code != 200:
                raise Exception

            product = product.json()
        except Exception:
            product = {}

        return product
