from flask_testing import TestCase

import settings
from app import app
from app.database import db
from app.models.client_model import ClientModel


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object(settings.Testing)
        return app

    def setUp(self):
        db.create_all()

        client = ClientModel()
        client.name = "admin"
        client.email = "admin@luizalabs.com"

        db.session.add(client)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
