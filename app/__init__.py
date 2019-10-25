from flask import Blueprint
from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from app.cli import configuration as config_cli
from app.database import configuration as config_database
from app.database import db
from app.error_handlers import configuration as config_error_handlers
from app.routes import import_routes
from app.models import import_models
from app.marshmallow import configuration as config_schema
from app.midlewares import configuration as config_middlewares
from app.migrate import configuration as config_migration
from app.restplus import configuration as config_resplus
from settings import load_config

# Initialize Flask
app = Flask(__name__, static_folder="static")
app.url_map.strict_slashes = False
blueprint = Blueprint("api", __name__, url_prefix=None)

# Proxy
app.wsgi_app = ProxyFix(app.wsgi_app)

# Configuration Cors
CORS(app, resources={r"/*": {"origins": "*"}})

# Load configuration
app.config.from_object(load_config())

# Initialize SQL Alchemy, Migration and import models
config_database(app=app)
config_migration(app=app, db=db)
import_models()

# Configuration Cli
config_cli(app=app)

# Initialize Marshmallow
config_schema(app=app)

# Initialize Restplus and import Routes
config_resplus(app=app, blueprint=blueprint)
import_routes()

# Configuration Middlewares and Error Handlers
config_middlewares(app=app)
config_error_handlers(app=app)
