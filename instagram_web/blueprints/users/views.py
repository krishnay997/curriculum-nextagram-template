from flask import Blueprint, render_template,redirect,request,url_for
from models.user import User
from werkzeug.security import generate_password_hash

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/new', methods=['POST'])
def create():
    mail=request.form.get("email")
    uname=request.form.get("username")
    password0=request.form.get("password")
    same_mail=User.get_or_none(User.email==mail)
    same_uname=User.get_or_none(User.username==uname)

    if same_mail:
        return render_template('users/new.html', errors=["Email is already taken!"])

    elif same_uname:
        return render_template('users/new.html', errors=["Username is already taken!"])

    elif len(password0)<6:
        return render_template('users/new.html', errors=["Password should be more than 6 characters!"])

    else:
        hashed_password = generate_password_hash(password0)
        User.create(first_name=request.form.get("first_name"),last_name=request.form.get("last_name"),email=mail,username=uname,password=hashed_password)
        return render_template('users/new.html', errors=[f"Welcome to Nextagram, {uname}!"])


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
