from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__ ="user"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username= db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    phonenum = db.Column(db.String(50),nullable= False)

class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))

    author = db.relationship("User",backref=db.backref("authors"))

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    is_ban = db.Column(db.Boolean,nullable=False,default=True)

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    question_id = db.Column(db.Integer,db.ForeignKey("question.id"))

    user = db.relationship("User",backref=db.backref("users"))
    question = db.relationship("Question",backref=db.backref("questions"))