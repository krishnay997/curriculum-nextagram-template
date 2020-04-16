import os
import config

from flask import Flask
from models.base_model import db
from flask_wtf.csrf import CsrfProtect
from flask import Blueprint, jsonify,render_template,request
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_identity)
from models.user import User,Images,Amount
from models.following import Following
from flask_cors import CORS,cross_origin

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')


app = Flask('NEXTAGRAM', root_path=web_dir)
app.config["JWT_SECRET_KEY"]="secret"
jwt=JWTManager(app)

cors = CORS(app,resources=r'/api/*')

app.config['CORS_HEADERS'] = 'Content-Type'


app.secret_key="secret"

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

csrf=CsrfProtect(app)

@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
