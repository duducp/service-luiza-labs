import subprocess
import os

import sqlalchemy

import click
from logzero import logger

import settings


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
            database_uri2 += "/postgres"

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

    @app.cli.group()
    def commands():
        """Useful commands like lint, tests and complexity"""

    @commands.command("lint")
    def lint():
        """Run Lint to arrange code according to PEP8"""
        _lint()

    @commands.command("coverage")
    def coverage():
        """Performs coverage tests"""
        _coverage()

    @commands.command("coverage-server")
    def coverage_server():
        """Start server to view tested files"""
        try:
            _coverage()
            _coverage_server()
        except KeyboardInterrupt:
            logger.info("Command canceled")

    @commands.command("complexity")
    def complexity():
        """Calculate the complexity of project methods"""
        _complexity()

    @commands.command("all")
    def all():
        """Runs Lint, complexity, and tests commands"""
        _lint()
        _complexity()
        _coverage()

    def _lint():
        try:
            logger.info("Running pre-commit...")
            subprocess.run(["pre-commit", "install"])
            subprocess.run(["pre-commit", "run", "--all-files"])
        except KeyboardInterrupt:
            logger.info("Command canceled")

    def _coverage():
        try:
            logger.info("Running tests...")
            subprocess.run(["coverage", "run", "-m", "unittest", "discover", "tests"])
            subprocess.run(["coverage", "report"])
        except KeyboardInterrupt:
            logger.info("Command canceled")

    def _complexity():
        try:
            logger.info("Calculating complexity...")
            subprocess.run(
                [
                    "radon",
                    "cc",
                    "-s",
                    "-a",
                    "-nb",
                    "--total-average",
                    "-e",
                    "venv*",
                    ".",
                ]
            )
        except KeyboardInterrupt:
            logger.info("Command canceled")

    def _coverage_server():
        try:
            logger.info("Generating files...")
            subprocess.run(["coverage", "html"])
            os.chdir(settings.basedir + "/htmlcov")
            subprocess.run(["python", "-m", "http.server"])
        except KeyboardInterrupt:
            logger.info("Command canceled")
