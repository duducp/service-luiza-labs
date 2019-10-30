import subprocess
import os

import sqlalchemy
from logzero import logger

import settings


def execute_command_database(database_uri, command):
    engine = sqlalchemy.create_engine(database_uri)
    conn = engine.connect()
    conn.execute("commit")
    conn.execute(command)
    conn.close()


def create_database(config, name: str):
    try:
        logger.info("Creating database...")
        database_uri = f"{config.DATABASE_ENGINE}"
        database_uri += f"://{config.DATABASE_USER}"
        database_uri += f":{config.DATABASE_PW}"
        database_uri += f"@{config.DATABASE_HOST}"
        database_uri += f":{config.DATABASE_PORT}"

        command = f"create database {name}"
        try:
            execute_command_database(database_uri, command)
        except Exception:
            database_uri += f"/postgres"
            execute_command_database(database_uri, command)
    except KeyboardInterrupt:
        logger.info("Command canceled")
    except Exception as e:
        logger.info(f"Could not create database. Reason: {str(e)}")


def install_extension_postgres(config, command: str = "create extension unaccent;"):
    try:
        logger.info("Installing extension...")
        database_uri = f"{config.DATABASE_ENGINE}"
        database_uri += f"://{config.DATABASE_USER}"
        database_uri += f":{config.DATABASE_PW}"
        database_uri += f"@{config.DATABASE_HOST}"
        database_uri += f":{config.DATABASE_PORT}"

        try:
            execute_command_database(database_uri, command)
        except Exception:
            database_uri += f"/postgres"
            execute_command_database(database_uri, command)
    except KeyboardInterrupt:
        logger.info("Command canceled")
    except Exception as e:
        logger.info(f"Could not install extension. Reason: {str(e)}")


def apply_database_migrations():
    try:
        logger.info("Applying migrations...")
        subprocess.run(["flask", "db", "upgrade"])
    except KeyboardInterrupt:
        logger.info("Command canceled")
    except Exception as e:
        logger.info(f"Could not apply migrations. Reason: {str(e)}")


def lint():
    try:
        logger.info("Running pre-commit...")
        subprocess.run(["pre-commit", "install"])
        subprocess.run(["pre-commit", "run", "--all-files"])
    except KeyboardInterrupt:
        logger.info("Command canceled")


def coverage():
    try:
        logger.info("Running tests...")
        subprocess.run(["coverage", "run", "-m", "unittest", "discover", "tests"])
        subprocess.run(["coverage", "report"])
    except KeyboardInterrupt:
        logger.info("Command canceled")


def complexity():
    try:
        logger.info("Calculating complexity...")
        subprocess.run(
            ["radon", "cc", "-s", "-a", "-nb", "--total-average", "-e", "venv*", "."]
        )
    except KeyboardInterrupt:
        logger.info("Command canceled")


def coverage_server():
    try:
        logger.info("Generating files...")
        subprocess.run(["coverage", "html"])
        os.chdir(settings.basedir + "/htmlcov")
        subprocess.run(["python", "-m", "http.server"])
    except KeyboardInterrupt:
        logger.info("Command canceled")
