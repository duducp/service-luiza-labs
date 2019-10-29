import json
from http import HTTPStatus

from app import db

import settings
from app.models.favorite_model import FavoriteModel
from app.persistence.redis_persistence import RedisPersistence
from app.schemas.models.favorite_schema import FavoriteSchema
from app.services.products_service import ProductService
from app.utils.format_response import Response


class FavoriteController:
    def __init__(self):
        self._config = settings.load_config()
        self._response = Response()
        self._product_service = ProductService()
        self._redis = RedisPersistence(db=self._config.REDIS_DB_FAVORITE)

    def get_all_by_client(self, client_id: str, args: dict):
        try:
            page = int(args.get("page", 1))
            per_page = int(args.get("limit", 10))

            favorites = self._redis.get(name=f"f-{client_id}", key=f"{page}-{per_page}")
            if favorites:
                favorites = json.loads(favorites)
            else:
                favorites = (
                    db.session.query(FavoriteModel)
                    .filter(FavoriteModel.client_id == client_id)
                    .paginate(page=page, per_page=per_page, max_per_page=100)
                )

                favorites = self._response.get_data_schema(
                    schema=FavoriteSchema(many=True), data=favorites
                )

                self._redis.delete_name(f"f-{client_id}")
                self._redis.set(
                    name=f"f-{client_id}", key=f"{page}-{per_page}", value=favorites
                )

            return self._response.send(
                status=HTTPStatus.OK,
                data=favorites,
                code="success",
                message="Favorites found successfully",
            )
        except Exception as e:
            raise e

    def get_all_by_client_details_product(self, client_id: str, args: dict):
        try:
            page = int(args.get("page", 1))
            per_page = int(args.get("limit", 10))

            favorites = self._redis.get(
                name=f"fd-{client_id}", key=f"{page}-{per_page}"
            )
            if favorites:
                favorites = json.loads(favorites)
            else:
                favorites = (
                    db.session.query(FavoriteModel)
                    .filter(FavoriteModel.client_id == client_id)
                    .paginate(page=page, per_page=per_page, max_per_page=100)
                )

                favorites = self._response.get_data_schema(
                    schema=FavoriteSchema(many=True), data=favorites
                )

                for favorite in favorites.get("results", []):
                    product_id = favorite.get("product_id", "")
                    product = self._get_data_product(product_id=product_id)
                    favorite["product"] = product

                self._redis.delete_name(f"fd-{client_id}")
                self._redis.set_expires(
                    key=f"{page}-{per_page}",
                    name=f"fd-{client_id}",
                    value=favorites,
                    expires_minutes=self._config.REDIS_DB_FAVORITE_DETAILS_EXPIRE,
                )

            return self._response.send(
                status=HTTPStatus.OK,
                data=favorites,
                code="success",
                message="Favorites found successfully",
            )
        except Exception as e:
            raise e

    def post(self, data: FavoriteModel):
        try:
            db.session.add(data)
            db.session.commit()

            self._redis.delete_name(f"f-{str(data.client_id)}")
            self._redis.delete_name(f"fd-{str(data.client_id)}")

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

            self._redis.delete_name(f"f-{client_id}")
            self._redis.delete_name(f"fd-{client_id}")

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
