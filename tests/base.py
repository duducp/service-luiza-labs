import sqlalchemy
from flask_testing import TestCase
from logzero import logger

import settings
from app import app
from app.database import db
from app.models.client_model import ClientModel


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object(settings.Testing)
        return app

    def setUp(self):
        self._create_database(name=settings.Testing.DATABASE_DB)

        db.create_all()

        client = ClientModel()
        client.id = "5945d7a6-306e-4f55-97e1-7a96de89d8d7"
        client.name = "admin"
        client.email = "admin@luizalabs.com"

        db.session.add(client)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_database(self, name):
        try:
            database_uri = f"{app.config.get('DATABASE_ENGINE')}"
            database_uri += f"://{app.config.get('DATABASE_USER')}"
            database_uri += f":{app.config.get('DATABASE_PW')}"
            database_uri += f"@{app.config.get('DATABASE_HOST')}"
            database_uri += f":{app.config.get('DATABASE_PORT')}"

            command = f"create database {name}"
            try:
                self._execute_command_postgres(database_uri, command)
            except Exception:
                database_uri += "/postgres"
                self._execute_command_postgres(database_uri, command)
        except Exception as e:
            logger.info(f"Could not create database. Reason: {str(e)}")

    @staticmethod
    def _execute_command_postgres(database_uri, command):
        engine = sqlalchemy.create_engine(database_uri)
        conn = engine.connect()
        conn.execute("commit")
        conn.execute(command)
        conn.close()
