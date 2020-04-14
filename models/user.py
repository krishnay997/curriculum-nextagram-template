from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from flask_login import UserMixin,current_user
from playhouse.hybrid import hybrid_property



def has_lower(word):
    return re.search("[a-z]", word)

def has_upper(word):
    return re.search("[A-Z]", word)

def has_special(word):
    return re.search("[\W]", word)


class User(UserMixin,BaseModel):
    first_name = pw.CharField(unique=False,null=False)
    last_name = pw.CharField(unique=False,null=False)
    username=pw.CharField(unique=True,null=False)
    email=pw.CharField(unique=True,null=False)
    password=pw.CharField(unique=False,null=False)
    real_password=None
    profile_pic=pw.TextField(null=True)

    def validate(self):
        same_mail=User.get_or_none(email=self.email)
        same_uname=User.get_or_none(username=self.username)

        if same_mail and self.id != same_mail.id:
            self.errors.append("Email is already taken!")

        if same_uname:
            self.errors.append("Username is already taken!")
        
        if len(self.password)<=6:
            self.errors.append("Password should be greater than 6 characters!")

        if not has_lower(self.password):
            self.errors.append("Password should contain lower characters!")

        if not has_upper(self.password):
            self.errors.append("Password should contain upper characters!")

        if not has_special(self.password):
            self.errors.append("Password should contain special characters!")

 
        if self.real_password is not None:
            self.password=generate_password_hash(self.password)

    @hybrid_property
    def profile_image_url(self):
        return self.profile_pic
    
    @hybrid_property
    def follower_requests(self):
        from models.following import Following
        return User.select().join(Following, on=(User.id==Following.follower_id)).where((Following.user_id==self.id) and (Following.approved==False))

    @hybrid_property
    def followers(self):
        from models.following import Following
        return User.select().join(Following, on=(User.id==Following.follower_id)).where((Following.user_id==self.id) and (Following.approved==True))

    @hybrid_property
    def following(self):
        from models.following import Following
        return User.select().join(Following, on=(User.id==Following.user_id)).where((Following.follower_id==self.id) and (Following.approved==True))

class Images(UserMixin,BaseModel):
    user = pw.ForeignKeyField(User, backref='images')
    image_path=pw.TextField(null=False)

class Amount(UserMixin,BaseModel):
    amount_donated=pw.IntegerField(null=False)
    donator_username=pw.TextField(null=False)
    recipient_username=pw.TextField(null=True)
    image_url=pw.TextField(null=True)

