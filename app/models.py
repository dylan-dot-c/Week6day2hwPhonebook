# file for our models
from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
# creating address model
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False, unique=True)
    address = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def to_dict(self):
        result = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'address': self.address,
            'date_created': self.date_created
        }

        return result


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_url = db.Column(db.String, nullable=False, default="https://i.pinimg.com/originals/ea/5b/30/ea5b30d9848f2bf980b061f11e0729f6.png")
    addresses = db.relationship('Address', backref='addresses')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs.get('password', ''))

    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)
    
    def __repr__(self):
        return f"<User {self.user_id}|{self.email}>"
    
    def get_id(self):
        return self.user_id
    
@login.user_loader
def get_user(user_id):
    return db.session.get(User, user_id)