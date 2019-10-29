import os

from dotenv import load_dotenv

load_dotenv(verbose=True)
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    ENVIRONMENT = os.getenv("ENVIRONMENT", "")

    # Flask
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))
    CSRF_ENABLED = os.getenv("CSRF_ENABLED", True)
    SECRET_KEY = os.getenv("SECRET_KEY", "e6cf6d81-a23c-4712-96c8-c8e6c79cf11f")

    # Restplus
    SWAGGER_TITLE = os.getenv("SWAGGER_TITLE", "Service Client Luiza Labs")
    SWAGGER_DESCRIPTION = os.getenv(
        "SWAGGER_DESCRIPTION",
        "Este serviço é responsável por cuidar dos clientes e seus produtos favoritos",
    )
    SWAGGER_UI_DOC_EXPANSION = "list"  # None, "list", "full"
    RESTPLUS_VALIDATE = False
    RESTPLUS_MASK_SWAGGER = False
    ERROR_INCLUDE_MESSAGE = False
    ERROR_404_HELP = False

    # Sql Alchemy
    DATABASE_ENGINE = os.getenv("DATABASE_ENGINE", "postgresql")
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT = int(os.getenv("DATABASE_PORT", "5432"))
    DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PW = os.getenv("DATABASE_PW", "postgres")
    DATABASE_DB = os.getenv("DATABASE_DB", "luizalabs")

    SQLALCHEMY_DATABASE_URI = f"{DATABASE_ENGINE}"
    SQLALCHEMY_DATABASE_URI += f"://{DATABASE_USER}"
    SQLALCHEMY_DATABASE_URI += f":{DATABASE_PW}"
    SQLALCHEMY_DATABASE_URI += f"@{DATABASE_HOST}"
    SQLALCHEMY_DATABASE_URI += f":{DATABASE_PORT}"
    SQLALCHEMY_DATABASE_URI += f"/{DATABASE_DB}"

    # Redis
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")
    REDIS_DB_AUTH = int(os.getenv("REDIS_DB_AUTH", "0"))
    REDIS_DB_FAVORITE = int(os.getenv("REDIS_DB_FAVORITE", "1"))
    REDIS_DB_FAVORITE_DETAILS_EXPIRE = int(
        os.getenv("REDIS_DB_FAVORITE_DETAILS_EXPIRE", "5")
    )

    # Others
    SERVICE_PRODUCTS = os.getenv(
        "SERVICE_PRODUCTS", "http://challenge-api.luizalabs.com/api/product"
    )

    TOKEN_ACCESS_EXP_MINUTES = int(os.getenv("TOKEN_ACCESS_EXP_MINUTES", "15"))
    TOKEN_REFRESH_EXP_MINUTES = int(os.getenv("TOKEN_REFRESH_EXP_MINUTES", "30"))


class Development(BaseConfig):
    ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME", "DESENVOLVIMENTO")
    SWAGGER_VISIBLE = os.getenv("SWAGGER_VISIBLE", True)
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", True)
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", True)
    TESTING = os.getenv("TESTING", False)
    DEBUG = os.getenv("DEBUG", True)
    FLASK_ENV = os.getenv("FLASK_ENV", "development")


class Production(BaseConfig):
    ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME", "PRODUÇÃO")
    SWAGGER_VISIBLE = os.getenv("SWAGGER_VISIBLE", False)
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", False)
    TESTING = os.getenv("TESTING", False)
    DEBUG = os.getenv("DEBUG", False)
    FLASK_ENV = os.getenv("FLASK_ENV", "production")


class Testing(BaseConfig):
    ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME", "TESTE")
    SWAGGER_VISIBLE = os.getenv("SWAGGER_VISIBLE", False)
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", True)
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", True)
    DEBUG = os.getenv("DEBUG", False)
    TESTING = os.getenv("TESTING", True)
    FLASK_ENV = os.getenv("FLASK_ENV", "testing")
    CSRF_ENABLED = os.getenv("CSRF_ENABLED", False)


def load_config():
    envs = {
        "develop": Development,
        "development": Development,
        "testing": Testing,
        "test": Testing,
        "production": Production,
        "master": Production,
    }

    return envs.get(BaseConfig.ENVIRONMENT, Development)
