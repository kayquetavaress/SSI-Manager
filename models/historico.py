from datetime import datetime
from models.usuario import db


class Historico(db.Model):

    __tablename__ = "historico"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    ssi_id = db.Column(
        db.Integer,
        nullable=False
    )

    usuario = db.Column(
        db.String(100),
        nullable=False
    )

    acao = db.Column(
        db.String(255),
        nullable=False
    )

    data = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )