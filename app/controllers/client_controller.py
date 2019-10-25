from http import HTTPStatus

from app import db

import settings
from app.models.client_model import ClientModel
from app.schemas.models.client_schema import ClientSchema
from app.utils.format_response import Response


class ClientController:
    def __init__(self):
        self._config = settings.load_config()
        self._response = Response()

    def get_all(self, args: dict):
        try:
            query = db.session.query(ClientModel)
            data = query.paginate(page=int(args.get('page', 1)), per_page=10, max_per_page=100)

            return self._response.send(
                status=HTTPStatus.OK,
                data=data,
                schema=ClientSchema(many=True),
            )
        except Exception as e:
            raise e

    def get_one(self, _id: str):
        try:
            data = db.session.query(ClientModel).first()
            if not data:
                return self._response.send(
                    message=f"Client '{_id}' not found",
                    status=HTTPStatus.NOT_FOUND,
                    code="not_found",
                )

            return self._response.send(
                schema=ClientSchema(),
                data=data,
                status=HTTPStatus.OK,
                code="success",
                message="Clients searched",
            )
        except Exception as e:
            raise e

    def post(self, data: ClientModel):
        try:
            db.session.add(data)
            db.session.commit()

            return self._response.send(
                schema=ClientSchema(),
                data=data,
                status=HTTPStatus.CREATED,
                code="success",
                message="Client created",
            )
        except Exception as e:
            db.session.rollback()
            raise e
        finally:
            db.session.close()

    def put(self, _id: str, data: ClientModel):
        try:
            db.session.add(data)
            db.session.commit()

            return self._response.send(
                schema=ClientSchema(),
                data=data,
                status=HTTPStatus.OK,
                code="success",
                message="Client updated",
            )
        except Exception as e:
            db.session.rollback()
            raise e
        finally:
            db.session.close()
