from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin , LoginManager
import sys
from datetime import datetime

login_manager = LoginManager()
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String())
    credentialDocs = db.relationship("CredentialDocs",backref="owner",cascade="all, delete-orphan")
    emailVerified = db.Column(db.Boolean)
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)



datetime.utcnow().timestamp()
class CredentialDocs(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    domainname = db.Column(db.String(20))
    credentials = db.Column(db.String)
    owner_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    lastUpdateTimeStamp = db.Column(
            db.Integer ,
            default=datetime.utcnow().timestamp(),
            onupdate=datetime.utcnow().timestamp()
            )
    __table_args__ = ((db.UniqueConstraint("owner_id","domainname")),)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
