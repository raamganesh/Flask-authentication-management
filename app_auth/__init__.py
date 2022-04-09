from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from decouple import Config, RepositoryEnv

DOTENV_FILE = '.env'
env_config = Config(RepositoryEnv(DOTENV_FILE))

db = SQLAlchemy()


def create_app():
    """Initialize flask context and database instance according to configurating and data models
    """
    app = Flask(__name__)
    # Google Cloud SQL (change this accordingly)
    PASSWORD = env_config.get("PASSWORD")
    PUBLIC_IP_ADDRESS = env_config.get("PUBLIC_IP_ADDRESS")
    DBNAME = env_config.get("DBNAME")
    PROJECT_ID = env_config.get("PROJECT_ID")
    INSTANCE_NAME = env_config.get("INSTANCE_NAME")

    # configuration
    app.config["SECRET_KEY"] = env_config.get("SECRET_KEY")
    app.config[
        "SQLALCHEMY_DATABASE_URI"] = f'mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .data_model import User, Insight

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
