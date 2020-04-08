from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from flask_login import UserMixin,current_user

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

