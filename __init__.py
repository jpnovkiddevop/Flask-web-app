from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .secret import siri
from .secretkey import mysiri

app = Flask(__name__)

# Set the PostgreSQL database URI
app.config['SQLALCHEMY_DATABASE_URI'] = siri
app.config['SECRET_KEY'] = mysiri

# If you want to suppress a warning, you can add the following line
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def create_app():
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


if __name__ == '__main__':
    create_app()  # Run the Flask app when the script is executed directly
