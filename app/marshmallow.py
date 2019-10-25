from flask_marshmallow import Marshmallow

ma = Marshmallow()


def configuration(app):
    ma.init_app(app)
