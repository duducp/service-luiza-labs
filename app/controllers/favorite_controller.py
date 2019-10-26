from http import HTTPStatus

from app import db

import settings
from app.models.favorite_model import FavoriteModel
from app.schemas.models.favorite_schema import FavoriteSchema
from app.utils.format_response import Response


class FavoriteController:
    def __init__(self):
        self._config = settings.load_config()
        self._response = Response()

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
                status=HTTPStatus.OK,
                data=data,
                schema=FavoriteSchema(many=True),
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
