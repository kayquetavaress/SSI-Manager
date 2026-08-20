from models.usuario import db

class Checklist(db.Model):

    __tablename__ = "checklist"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    ssi_id = db.Column(
        db.Integer,
        nullable=False
    )

    analisado = db.Column(
        db.Boolean,
        default=False
    )

    evidencia = db.Column(
        db.Boolean,
        default=False
    )

    correcao = db.Column(
        db.Boolean,
        default=False
    )

    teste = db.Column(
        db.Boolean,
        default=False
    )

    validacao = db.Column(
        db.Boolean,
        default=False
    )

    encerramento = db.Column(
        db.Boolean,
        default=False
    )