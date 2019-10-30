import click
from logzero import logger

import settings
from app.utils.commands import (
    create_database,
    install_extension_postgres,
    apply_database_migrations,
    lint,
    coverage,
    coverage_server,
    complexity,
)


def configuration(app):
    @app.cli.group()
    def config():
        """Commands with project settings"""

    @config.command("create-db")
    @click.argument("name")
    def config_create_db(name):
        """
        Create the database PostgreSQL
        """
        config = settings.load_config()
        create_database(name=name, config=config)

    @config.command("unaccent")
    def config_create_extension_unaccent():
        """
        Install the unaccess extension in PostgreSQL
        """
        config = settings.load_config()
        install_extension_postgres(config=config, command="create extension unaccent;")

    @config.command("migration")
    def config_apply_migrations():
        """
        Apply database migrations
        """
        apply_database_migrations()

    @app.cli.group()
    def commands():
        """Useful commands like lint, tests and complexity"""

    @commands.command("lint")
    def commands_lint():
        """Run Lint to arrange code according to PEP8"""
        lint()

    @commands.command("coverage")
    def commands_coverage():
        """Performs coverage tests"""
        coverage()

    @commands.command("coverage-server")
    def commands_coverage_server():
        """Start server to view tested files"""
        try:
            coverage()
            coverage_server()
        except KeyboardInterrupt:
            logger.info("Command canceled")

    @commands.command("complexity")
    def commands_complexity():
        """Calculate the complexity of project methods"""
        complexity()

    @commands.command("all")
    def commands_all():
        """Runs Lint, complexity, and tests commands"""
        lint()
        complexity()
        coverage()
