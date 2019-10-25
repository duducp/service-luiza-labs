from http import HTTPStatus

from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import NotFound

from app.utils.format_response import Response


def configuration(app):
    @app.api.errorhandler(NoResultFound)
    def database_not_found_error_handler(e):
        return Response().send(
            data=str(e),
            message="A database result was required but none was found.",
            code="item_not_found",
            status=HTTPStatus.NOT_FOUND,
        )

    @app.api.errorhandler(NotFound)
    def not_found(e):
        return Response().send(
            data=None,
            message=e.description,
            code=str(e.name).replace(" ", "_").lower(),
            status=e.code,
        )

    @app.api.errorhandler(Conflict)
    def conflict(e):
        return Response().send(
            data=None,
            message=e.description,
            code=str(e.name).replace(" ", "_").lower(),
            status=e.code,
        )

    @app.api.errorhandler
    def default_error_handler(e):
        raise Exception(e)
