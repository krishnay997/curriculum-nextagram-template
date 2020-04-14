from flask import Blueprint, render_template,redirect,request,url_for,flash
from models.user import User,Images
from models.following import Following
from flask_login import login_user,logout_user,login_required,current_user
import os
import boto3
import botocore
import datetime


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
    follow=Following.select().where(Following.user_id==current_user.id).where(Following.approved == False)
    
    print("************************************************************************************")
    for f in follow:
        print(f.follower_id)
    print("************************************************************************************")
    check=User.get_or_none(User.username==username)
    if check is not None:
        return render_template("users/profile.html",username=username,picture=check.profile_pic,user=check,current_user=current_user,follow=follow)
    else:
        flash("User does not exist.")
        return redirect(url_for("home"))

@users_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    get_user=User.get_or_none(User.username==request.form.get("search"))
    if request.method == 'POST' and get_user is not None:
        return redirect(url_for("users.show",username=get_user.username))
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

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("S3_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY")
)

@users_blueprint.route("/profpic", methods=["GET"])
@login_required
def profpic():
    return render_template("users/upload_profpic.html")

@users_blueprint.route("/upload", methods=["POST"])
@login_required
def upload():
    try:
        file = request.files.get("img")
        s3.upload_fileobj(
            file,
            "krishnaybucket",
            file.filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )
        user=User.get_or_none(User.id==current_user.id)
        user.update(updated_at=datetime.datetime.now(),profile_pic=f"http://krishnaybucket.s3.amazonaws.com/{file.filename}").where(User.id==current_user.id).execute()
        
        return redirect(url_for("home"))
        
    except Exception as e:

        print("Something Happened: ", e)
        flash("Cannot upload nothing")
        return redirect(url_for("home"))


@users_blueprint.route("/upload/images", methods=["POST"])
@login_required
def upload_images():
    try:
        file = request.files.get("imgs")
        s3.upload_fileobj(
            file,
            "krishnaybucket",
            file.filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )
        user=User.get_or_none(User.id==current_user.id)
        Images.create(image_path=f"http://krishnaybucket.s3.amazonaws.com/{file.filename}",user=user)
        
        return redirect(url_for("home"))
        
    except Exception as e:

        print("Something Happened: ", e)
        flash("Cannot upload nothing")
        return redirect(url_for("home"))



@users_blueprint.route("/follow/<user_id>", methods=["POST"])
@login_required
def follow(user_id):
    follow=Following(user_id=user_id,follower_id=current_user.id)
    follow.save()
    flash("Request sent for approval")
    user_prof=User.get_or_none(User.id==user_id)
    return redirect(url_for("users.show",username=user_prof.username))


@users_blueprint.route("/accept/<user_id>", methods=["POST"])
@login_required
def accept(user_id):
    follow=Following.get(Following.id==user_id)
    follow.approved=True
    follow.save()
    return redirect(url_for("users.show",username=current_user.username))

