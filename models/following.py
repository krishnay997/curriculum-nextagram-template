from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from flask_login import UserMixin,current_user
from playhouse.hybrid import hybrid_property
from models.user import User


class Following(BaseModel):
    user=pw.ForeignKeyField(User)
    follower=pw.ForeignKeyField(User)
    approved=pw.BooleanField(default=False)

    def validate(self):
        if self.user_id==self.follower_id:
            self.errors.append("Cannot follow self")