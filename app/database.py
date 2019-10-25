from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def configuration(app):
    db.init_app(app)
    app.db = db
