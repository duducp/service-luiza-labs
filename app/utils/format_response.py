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
        if status == 204:
            data = {}
        elif schema:
            data = self.get_data_schema(schema=schema, data=data)
            data = json.loads(json.dumps(data, default=format_encoder_object))
            data = {
                "status": status,
                "message": message,
                "code": code,
                "data": data,
            }

        headers = self.__format_headers(headers)
        return make_response(json.dumps(data), status, headers)

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

    def get_data_schema(self, schema, data):
        if isinstance(data, Pagination):
            results = schema.dump(data.items)
            if results:
                results = results.data

            data = self._format_paginate(
                results=results,
                page=data.page,
                size=data.per_page,
                total_items=data.total,
                total_pages=data.pages,
            )
        else:
            data = schema.dump(data).data

        return data

    @staticmethod
    def _format_paginate(results, page, size, total_items, total_pages) -> dict:
        return {
            "results": results,
            "page": page,
            "size": size,
            "total_items": total_items,
            "total_pages": total_pages,
        }
