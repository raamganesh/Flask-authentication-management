from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # Google Cloud SQL (change this accordingly)
    PASSWORD = "test"
    PUBLIC_IP_ADDRESS = "35.202.93.195"
    DBNAME = "testdb"
    PROJECT_ID = "fluted-cogency-340019"
    INSTANCE_NAME = "test"

    # configuration
    # app.config["SECRET_KEY"] = "Y9bezJhzYMIovBRfv2Tmb+JvsgKbYqS7dwML/yKd"
    app.config[
        "SQLALCHEMY_DATABASE_URI"] = f'mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .user_model import User

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
