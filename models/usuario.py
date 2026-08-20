from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    senha = db.Column(
        db.String(255),
        nullable=False
    )