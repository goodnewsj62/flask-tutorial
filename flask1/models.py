from flask1 import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    email = db.Column(db.String(30), unique = True, nullable = False)
    password = db.Column(db.String(30), nullable = False )
    post = db.relationship('Post', backref = 'writer', lazy = True)

    def __repr__(self):
        return "User('{0.username!r}','{0.email!r}')".format(self)
    def __str__(self):
        return f'{self.username}'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(40), nullable = False )
    content = db.Column(db.Text, nullable = False )
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False )

    def __repr__(self):
        return 'Post({title_},{id_})'.format(title_ = self.title,id_ = self.id)
