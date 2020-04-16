from flask import Blueprint, jsonify,render_template,request,redirect
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_identity)
from models.user import User,Images,Amount
from models.following import Following
from flask_wtf.csrf import CsrfProtect
from app import app
from app import csrf
from app import cors,cross_origin,CORS
from werkzeug.security import generate_password_hash,check_password_hash
import ast

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')


@users_api_blueprint.route('/', methods=['GET'])

def get_all_users():
    users=User.select()
    result=[]
    for user in users:
        user_info={}
        user_info["id"]=user.id
        user_info["username"]=user.username
        user_info["profileImage"]=user.profile_pic
        result.append(user_info)
    return jsonify(result)

@users_api_blueprint.route('/<id>', methods=['GET'])
def get_one_users(id):
    user=User.get_or_none(User.id==id)

    if user is None:
        return jsonify({"message":"No user found!"})
    else:
        user_info={}
        user_info["id"]=user.id
        user_info["username"]=user.username
        user_info["profileImage"]=user.profile_pic
        return jsonify({"user":user_info})

@users_api_blueprint.route('/me', methods=['GET'])
@jwt_required
def get_current_user():
    current_user=get_jwt_identity()
    
    user=User.get_or_none(User.username==current_user)

    if user is None:
        return jsonify({"message":"No user found!"})
    else:
        user_info={}
        user_info["email"]=user.email
        user_info["id"]=user.id
        user_info["profile_picture"]=user.profile_pic
        user_info["username"]=user.username
        return jsonify(user_info)

@users_api_blueprint.route('/images/me', methods=['GET'])
@jwt_required
@csrf.exempt
@cross_origin()
def get_current_user_pics():
    current_user=get_jwt_identity()
    result=[]
    user=User.get_or_none(User.username==current_user)
    if user:
        for u in user.images:
            result.append(u.image_path)
        return jsonify(result)
    else:
        return jsonify({"message":"No images found!"})

@users_api_blueprint.route('/login/new')

@csrf.exempt

def login_page():
    return redirect("/login")

@users_api_blueprint.route("/login", methods=['POST'])
@csrf.exempt
@cross_origin()
def login():
    data = request.json
    
    uname=data.get("username")
    password=data.get("password")

    check=User.get_or_none(User.username==uname)
    result=check_password_hash(check.password,password)
    
    if check and result == True:
        access_token=create_access_token(identity=check.username)
        
        return jsonify(access_token=access_token,username=uname)
        
    else:
        return jsonify(message=f"{check}")



@users_api_blueprint.route("/upload", methods=['POST'])
@csrf.exempt
@cross_origin()
@jwt_required
def upload_image():
    current_user=get_jwt_identity()
    user=User.get_or_none(User.username==current_user)
    data = request.files["image"].filename
    print("*****************************************TESTING*******************************************")
    print(data)
    print("*****************************************TESTING*******************************************")
    data_image=data
    if user:
        result={}
        Images.create(image_path=f"http://krishnaybucket.s3.amazonaws.com/{data_image}",user=user)
        result["image_url"]=data_image
        result["success"]=True
        return jsonify(result)
    else:
        result={}
        result["message"]="No image provided"
        result["success"]="failed"
        return jsonify(result)



    
@users_api_blueprint.route("/new", methods=['POST'])
@csrf.exempt
@cross_origin()
def new():
    data = request.json
    print(data)
    uname=data.get("username")
    password=data.get("password")
    email=data.get("email")

    # No first name and last name because react sign up only has username, password and email field
    if uname:
        access_token=create_access_token(identity=uname)
        User.create(username=uname,password=password,email=email)
        return jsonify(access_token=access_token,username=uname)
        
    else:
        return jsonify(message=f"{uname}")
