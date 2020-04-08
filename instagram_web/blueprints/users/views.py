from flask import Blueprint, render_template,redirect,request,url_for,flash
from models.user import User
from flask_login import login_user,logout_user,login_required,current_user

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
    password=request.form.get("password")
    
    user=User(first_name=request.form.get("first_name"),last_name=request.form.get("last_name"),email=mail,username=uname,password=password, real_password=password)

    if user.save():
        flash(f"Welcome to nextagram {user.username}!")
        return redirect(url_for("users.new"))
    
    else:
        for e in user.errors:
            flash(e)
        return redirect(url_for("users.new"))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    check=User.select().where(User.username==username)
    if check:
        return render_template("users/profile.html",username=username)
    else:
        flash("User does not exist.")
        return redirect(url_for("home"))


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    id_num=int(id)
    if id_num==current_user.id:
        return render_template("users/edit.html")

    else:
        flash("Unauthorized to make changes.")
        return redirect(url_for("home"))



@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    uname=request.form.get("username")
    password=request.form.get("password")
    check=User.get_or_none(User.username==uname)
 
    if not check :
        user_change =User.get_or_none(User.id==current_user.id)
        user_change.username=uname
        user_change.password=password
        user_change.real_password=password
        user_change.save()
        print("test------------------------------------------------------")
        print(user_change.username)
        print("test------------------------------------------------------")
        flash("Saved changes")
        return render_template("users/profile.html",username=user_change.username)
    
    else:
        flash("Username already exists")
        return redirect(url_for("home"))

