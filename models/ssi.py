from datetime import datetime
from models.usuario import db


class SSI(db.Model):

    __tablename__ = "ssi"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    numero_ssi = db.Column(
        db.String(20),
        unique=True
    )

    chamado = db.Column(
        db.String(50)
    )

    solicitante = db.Column(
        db.String(100)
    )

    area = db.Column(
        db.String(100)
    )

    responsavel = db.Column(
        db.String(100)
    )

    prioridade = db.Column(
        db.String(20)
    )

    status = db.Column(
        db.String(30)
    )

    problema = db.Column(
        db.Text
    )

    data_abertura = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    data_encerramento = db.Column(
        db.DateTime
    )

    imagem = db.Column(
        db.String(255)
    )

    evidencia_fechamento = db.Column(
        db.String(255)
    )