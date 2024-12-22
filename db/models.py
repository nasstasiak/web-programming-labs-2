from . import db
from flask_login import UserMixin

class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(30), nullable = False, unique = True)
    password = db.Column(db.String(162), nullable = False)

    
class articles(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    login_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(50), nullable = False)
    article_text = db.Column(db.Text, nullable = False)
    is_favorite = db.Column(db.Boolean)
    is_public = db.Column(db.Boolean)
    likes = db.Column(db.Integer)


# Новая модель для книг
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String(255), nullable=False)
    cover_image = db.Column(db.String(255), nullable=False)