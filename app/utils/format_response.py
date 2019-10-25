import json

from flask import make_response
from flask import redirect
from flask_sqlalchemy import Pagination

from app.utils.format_encoder_object import format_encoder_object


class Response:
    def __init__(self):
        self.headers = {"Content-Type": "application/json"}

    def send(
        self,
        data=None,
        status=200,
        message: str = None,
        code: str = None,
        headers=None,
        schema=None,
    ):
        if schema:
            if isinstance(data, Pagination):
                results = schema.dump(data.items)
                if results:
                    results = results.data

                data = {
                    "results": results,
                    "page": data.page,
                    "size": data.per_page,
                    "total_items": data.total,
                    "total_pages": data.pages,
                }
            else:
                data = schema.dump(data).data

        if status in [204]:
            response = {}
        else:
            data = json.dumps(data, default=format_encoder_object)
            data = json.loads(data)

            response = {
                "status": status,
                "message": message,
                "code": code,
                "data": data,
            }

        headers = self.__format_headers(headers)
        return make_response(json.dumps(response), status, headers)

    @staticmethod
    def redirect(url, code=302):
        return redirect(url, code=code)

    def __format_headers(self, headers=None) -> dict:
        if headers is None:
            headers = {}

        try:
            for k, v in self.headers.items():
                if k.lower() not in list(map(str.lower, headers.keys())):
                    headers[k] = v
        except Exception:
            headers = self.headers
        finally:
            return headers
