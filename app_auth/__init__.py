from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()



def create_app():
    app = Flask(__name__)
    # Google Cloud SQL (change this accordingly)
    PASSWORD = "testdb"
    PUBLIC_IP_ADDRESS = "34.136.125.141"
    DBNAME = "testing"
    PROJECT_ID = "dark-foundry-344018"
    INSTANCE_NAME = "testdb"

    # configuration
    app.config["SECRET_KEY"] = "Y9bezJhzYMIovBRfv2Tmb+JvsgKbYqS7dwML/yKd"
    app.config[
        "SQLALCHEMY_DATABASE_URI"] = f'mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from user_model import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
