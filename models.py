
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('taco.db')


class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField(max_length=100)
    is_admin = BooleanField(default=False)
    
    class Meta:
        database = DATABASE
        
    @classmethod
    def create_user(cls, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password)
                )
        except IntegrityError:
            raise ValueError("User already exists.")
            

class Taco(Model):
    user = ForeignKeyField(
        rel_model=User,
        related_name='tacos'
    )
    protein = CharField()
    shell = CharField()
    cheese = BooleanField(default=False)
    extras = TextField()
    
    class Meta:
        database = DATABASE
    
    
def initialize():
    DATABASE.get_conn()
    DATABASE.create_tables([User, Taco], safe=True)
    DATABASE.close()
    
    
    
    
    
    
    
    
    
    
    