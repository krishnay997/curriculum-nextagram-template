from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.session.views import session_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from flask_login import LoginManager,UserMixin
from models.user import User

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id==user_id)

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(session_blueprint,url_prefix="/")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def no_url(e):
    return render_template('404.html'), 404


@app.route("/")
def home():
    return render_template('home.html')
