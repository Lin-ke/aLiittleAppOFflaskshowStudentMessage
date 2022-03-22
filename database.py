# -- coding:UTF-8 --
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

#Student表
class Student(db.Model):
    num = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    ssex = db.Column(db.String(10),nullable = False)
    cls = db.Column(db.String(30),nullable = False)
    depart = db.Column(db.String(30),nullable = False)
    addr = db.Column(db.String(80),nullable = False)
    def __repr__(self):
        return '<User %r>' % self.num
