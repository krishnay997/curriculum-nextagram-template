from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    first_name = pw.CharField(unique=False,null=False)
    last_name = pw.CharField(unique=False,null=False)
    username=pw.CharField(unique=True,null=False)
    email=pw.CharField(unique=True,null=False)
    password=pw.CharField(unique=False,null=False)
