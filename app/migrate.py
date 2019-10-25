from flask_migrate import Migrate


def configuration(app, db):
    Migrate(app, db)
