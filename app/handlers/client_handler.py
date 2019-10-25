from flask import request

from app.controllers.client_controller import ClientController
from app.models.client_model import ClientModel
from app.schemas.models.client_schema import ClientSchema
from app.utils.format_response import Response


class ClientHandler:
    def __init__(self):
        self._controller = ClientController()
        self._response = Response()

    def get_all(self):
        args = request.args.to_dict()
        return self._controller.get_all(args=args)

    def get_one(self, _id: str):
        return self._controller.get_one(_id=_id)

    def delete(self, _id: str):
        return self._controller.delete(_id=_id)

    def post(self):
        body = request.get_json(silent=True, force=True)
        data, errors = ClientSchema().load(data=body)
        if errors:
            return self._response.send(
                data=errors,
                status=400,
                message="The body does not match the scheme",
                code="body_incorrect",
            )

        return self._controller.post(data=data)

    def put_patch(self, _id: str, partial: bool):
        body = request.get_json(silent=True, force=True)

        data, errors = ClientSchema().load(
            data=body,
            instance=ClientModel().query.get(_id),
            partial=partial,
            many=False,
        )

        if errors:
            return self._response.send(
                data=errors,
                status=400,
                message="The body does not match the scheme",
                code="body_incorrect",
            )

        if not data.id:
            return self._response.send(
                message=f"item '{_id}' not found", status=404, code="item_not_found"
            )

        return self._controller.put(_id=_id, data=data)
