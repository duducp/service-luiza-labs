import sqlalchemy

import click
from logzero import logger


def configuration(app):
    @app.cli.group()
    def config():
        """Commands with project settings"""

    @config.command("create-db")
    @click.argument("name")
    def create_database(name):
        """
        Create the database PostgreSQL
        """
        try:
            database_uri = f"{app.config.get('DATABASE_ENGINE')}"
            database_uri += f"://{app.config.get('DATABASE_USER')}"
            database_uri += f":{app.config.get('DATABASE_PW')}"
            database_uri += f"@{app.config.get('DATABASE_HOST')}"
            database_uri += f":{app.config.get('DATABASE_PORT')}"

            database_uri2 = database_uri
            database_uri2 += f"/postgres"

            command = f"create database {name}"
            try:
                execute_command_postgres(database_uri, command)
            except Exception:
                execute_command_postgres(database_uri2, command)
            finally:
                logger.info(f"Database {name} created")
        except KeyboardInterrupt:
            logger.info("Command canceled")
        except Exception as e:
            logger.info(f"Could not create database. Reason: {str(e)}")

    @config.command("unaccent")
    def create_extension_unaccent():
        """
        Install the unaccess extension in PostgreSQL
        """
        try:
            database_uri = f"{app.config.get('DATABASE_ENGINE')}"
            database_uri += f"://{app.config.get('DATABASE_USER')}"
            database_uri += f":{app.config.get('DATABASE_PW')}"
            database_uri += f"@{app.config.get('DATABASE_HOST')}"
            database_uri += f":{app.config.get('DATABASE_PORT')}"

            database_uri2 = database_uri
            database_uri2 += f"/postgres"

            command = "create extension unaccent;"
            try:
                execute_command_postgres(database_uri, command)
            except Exception:
                execute_command_postgres(database_uri2, command)
            finally:
                logger.info("Extension installed.")
        except KeyboardInterrupt:
            logger.info("Command canceled")
        except Exception as e:
            logger.info(f"Could not install extension. Reason: {str(e)}")

    def execute_command_postgres(database_uri, command):
        engine = sqlalchemy.create_engine(database_uri)
        conn = engine.connect()
        conn.execute("commit")
        conn.execute(command)
        conn.close()
