from http import HTTPStatus

from flask import request
from sqlalchemy.exc import DataError, ProgrammingError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from werkzeug.routing import RequestRedirect

from app.utils.format_response import Response


def configuration(app):
    @app.before_request
    def before_request():
        if request.method in ("POST", "PUT", "PATCH"):
            body = request.get_json(silent=True, force=True)
            if not body:
                return Response().send(
                    status=HTTPStatus.BAD_REQUEST,
                    message="The request body must be informed",
                    code="body_not_informed",
                )

    @app.after_request
    def after_request(response):
        """
        Function triggered when the request is finish, in this case to prevent cache
        """
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Cache-Control"] = "no-store"
        response.headers["Pragma"] = "no-cache"
        response.headers["Server"] = "no-server"
        return response

    @app.errorhandler(Exception)
    def handle_exception(err):
        if isinstance(err, IntegrityError):
            if err.orig.pgcode == "23502":
                return Response().send(
                    message=err.orig.diag.message_primary,
                    code="field_required_not_informed",
                    data={"column_name": [err.orig.diag.column_name]},
                    status=HTTPStatus.BAD_REQUEST,
                )
            elif err.orig.pgcode == "23503":
                return Response().send(
                    message=err.orig.diag.message_detail,
                    code="constraint_key_informed_not_exists",
                    data={"constraint_name": [err.orig.diag.constraint_name]},
                    status=HTTPStatus.UNPROCESSABLE_ENTITY,
                )
            elif err.orig.pgcode == "23505":
                return Response().send(
                    message=err.orig.diag.message_detail,
                    code="duplicated_key",
                    data={"constraint_name": [err.orig.diag.constraint_name]},
                    status=HTTPStatus.CONFLICT,
                )
            else:
                return Response().send(
                    code="integrity_error", status=HTTPStatus.INTERNAL_SERVER_ERROR
                )

        elif isinstance(err, DataError):
            if err.orig.pgcode == "22P02":
                return Response().send(
                    message=err.orig.diag.message_primary,
                    status=HTTPStatus.BAD_REQUEST,
                    code="data_error",
                )
            else:
                return Response().send(
                    code="data_error", status=HTTPStatus.INTERNAL_SERVER_ERROR
                )

        elif isinstance(err, ProgrammingError):
            return Response().send(
                code="programming_error",
                message=str(err),
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        elif isinstance(err, NotFound):
            return Response().send(
                code="not_found",
                status=HTTPStatus.NOT_FOUND,
                message="The route you entered was not found",
            )

        elif isinstance(err, RequestRedirect):
            return err

        else:
            return Response().send(
                code="internal_error",
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                message=str(err),
            )
