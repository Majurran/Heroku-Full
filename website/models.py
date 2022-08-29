from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


############################ Previous Schemas Placeholder ############################
# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(150), unique=True)
#     password = db.Column(db.String(150))
#     first_name = db.Column(db.String(150))
#     notes = db.relationship('Note')

############################ New Schemas ############################
class NursingHome(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_list = db.Column(db.String(10000))     # In CSV format, e.g -> "bowling,tennis,golf,bike,tea,chess"
    wellbeing_list = db.Column(db.String(10000))    # In CSV format, e.g -> "flat,very-sad,happy,sick,sad,angry"
    name = db.Column(db.String(10000), unique=True)
    users = db.relationship('User')
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    nursing_home_id = db.Column(db.Integer, db.ForeignKey(NursingHome.id))
    
# Could probably combine the activity and the wellbeing schema together and have a text column that says one of the following: activity, wellbeing, food
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    name = db.Column(db.String(150), unique=True)
    nursing_home_id = db.Column(db.Integer, db.ForeignKey(NursingHome.id))
    
class Wellbeing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    name = db.Column(db.String(150), unique=True)
    nursing_home_id = db.Column(db.Integer, db.ForeignKey(NursingHome.id))
    