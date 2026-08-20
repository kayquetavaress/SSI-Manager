from datetime import datetime
import os
from models.historico import Historico 
from flask import flash

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename
from models.usuario import db, Usuario
from models.ssi import SSI

app = Flask(__name__)

app.config["SECRET_KEY"] = "ssi_fortlev_2026"

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ssi.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        senha = request.form["senha"]

        user = Usuario.query.filter_by(
            username=usuario
        ).first()

        if user and check_password_hash(
            user.senha,
            senha
        ):

            login_user(user)

            return redirect(
                url_for("dashboard")
            )

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():

    total_ssi = SSI.query.count()

    abertos = SSI.query.filter(
        SSI.status != "Concluído"
    ).count()

    concluidos = SSI.query.filter_by(
        status="Concluído"
    ).count()

    pendentes = abertos

    ultimos = SSI.query.order_by(
        SSI.id.desc()
    ).limit(5).all()

    return render_template(
        "dashboard.html",
        usuario=current_user,
        total_ssi=total_ssi,
        abertos=abertos,
        concluidos=concluidos,
        pendentes=pendentes,
        ultimos=ultimos
    )

@app.route("/novo_ssi", methods=["GET", "POST"])
@login_required
def novo_ssi():

    if request.method == "POST":

        imagem = request.files.get("imagem")

        nome_arquivo = None

        if imagem and imagem.filename:

            nome_arquivo = secure_filename(
                imagem.filename
            )

            upload_dir = os.path.join(
                app.root_path,
                "static",
                "uploads"
            )

            os.makedirs(
                upload_dir,
                exist_ok=True
            )

            imagem.save(
                os.path.join(
                    upload_dir,
                    nome_arquivo
                )
            )

            novo = SSI(

            numero_ssi=f"SSI-{SSI.query.count()+1:04d}",

            chamado="N/A",

            solicitante=request.form["solicitante"],

            area=request.form["area"],

            responsavel=request.form["responsavel"],

            prioridade=request.form["prioridade"],

            status="Aberto",

            problema=request.form["problema"],

            imagem=nome_arquivo

)

        db.session.add(novo)
        db.session.commit()

        historico = Historico(
            ssi_id=novo.id,
            usuario=current_user.username,
            acao="SSI criada"
        )

        db.session.add(historico)
        db.session.commit()

        return redirect(
            url_for("consulta")
        )

    return render_template(
        "novo_ssi.html"
    )


@app.route("/consulta")
@login_required
def consulta():

    registros = SSI.query.order_by(
        SSI.id.desc()
    ).all()

    return render_template(
        "consulta.html",
        registros=registros
    )

@app.route("/detalhes/<int:ssi_id>")
@login_required
def detalhes(ssi_id):

    ssi = SSI.query.get_or_404(ssi_id)

    historicos = Historico.query.filter_by(
        ssi_id=ssi.id
    ).order_by(
        Historico.data.desc()
    ).all()

    return render_template(
        "detalhes.html",
        ssi=ssi,
        historicos=historicos
    )
    
    
         
@app.route(
    "/resolver/<int:ssi_id>",
    methods=["POST"]
)
@login_required
def resolver_ssi(ssi_id):

    ssi = SSI.query.get_or_404(ssi_id)

    evidencia = request.files.get("evidencia")

    if not evidencia or not evidencia.filename:

        flash(
            "É obrigatório anexar uma evidência para concluir a SSI."
        )

        return redirect(
            url_for(
                "detalhes",
                ssi_id=ssi.id
            )
        )

    nome_arquivo = secure_filename(
        evidencia.filename
    )

    upload_dir = os.path.join(
        app.root_path,
        "static",
        "uploads"
    )

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    evidencia.save(
        os.path.join(
            upload_dir,
            nome_arquivo
        )
    )

    ssi.status = "Concluído"

    ssi.data_encerramento = datetime.utcnow()

    ssi.evidencia_fechamento = nome_arquivo

    db.session.commit()

    historico = Historico(
        ssi_id=ssi.id,
        usuario=current_user.username,
        acao="SSI resolvida com evidência"
    )

    db.session.add(historico)
    db.session.commit()

    return redirect(
        url_for(
            "detalhes",
            ssi_id=ssi.id
        )
    )
    
@app.route("/abertas")
@login_required
def ssi_abertas():

    registros = SSI.query.filter(
        SSI.status != "Concluído"
    ).all()

    return render_template(
        "consulta.html",
        registros=registros
    )

  
@app.route("/concluidas")
@login_required
def ssi_concluidas():

    registros = SSI.query.filter_by(
    status="Concluído"
    ).all()

    return render_template(
        "consulta.html",
        registros=registros
    )
    
@app.route("/excluir/<int:ssi_id>")
@login_required
def excluir_ssi(ssi_id):

    ssi = SSI.query.get_or_404(ssi_id)

    db.session.delete(ssi)
    db.session.commit()

    return redirect(
        url_for("consulta")
    )    
    
@app.route("/evidencias")
@login_required
def evidencias():

    return render_template(
        "evidencias.html"
    )


@app.route("/relatorios")
@login_required
def relatorios():

    return "<h1>Relatórios</h1>"


@app.route("/admin")
@login_required
def admin():

    return "<h1>Administração</h1>"



@app.route("/configuracoes")
@login_required
def configuracoes():
     return render_template("configuracoes.html")
 
 
 
@app.route("/usuarios", methods=["GET", "POST"])
@login_required
def usuarios():

    if current_user.username != "admin":

        flash(
            "Você não possui permissão para acessar esta página."
        )

        return redirect(
            url_for("dashboard")
        )

    if request.method == "POST":

        username = request.form["username"].strip()
        senha = request.form["senha"]

        existe = Usuario.query.filter_by(
            username=username
        ).first()

        if existe:

            flash("Usuário já existe.")

            return redirect(
                url_for("usuarios")
            )

        novo_usuario = Usuario(
            username=username,
            senha=generate_password_hash(senha)
        )

        db.session.add(novo_usuario)
        db.session.commit()

        flash("Usuário criado com sucesso.")

        return redirect(
            url_for("usuarios")
        )

    usuarios = Usuario.query.order_by(
        Usuario.username
    ).all()

    return render_template(
        "usuarios.html",
        usuarios=usuarios
    )
    
    
@app.route("/excluir_usuario/<int:user_id>")
@login_required
def excluir_usuario(user_id):

    if current_user.username != "admin":

        flash(
            "Você não possui permissão para executar esta ação."
        )

        return redirect(
            url_for("dashboard")
        )

    usuario = Usuario.query.get_or_404(
        user_id
    )

    if usuario.username == "admin":

        flash(
            "O usuário admin não pode ser excluído."
        )

        return redirect(
            url_for("usuarios")
        )

    db.session.delete(usuario)
    db.session.commit()

    flash(
        "Usuário excluído com sucesso."
    )

    return redirect(
        url_for("usuarios")
    )

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("login")
    )


if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        admin = Usuario.query.filter_by(
            username="admin"
        ).first()

        if not admin:

            admin = Usuario(
                username="admin",
                senha=generate_password_hash(
                    "123456"
                )
            )

            db.session.add(admin)
            db.session.commit()

    por = int(os.environ.get("PORT", 5000))
    
    app.run(
        host="0.0.0.0",
        port=por,
        debug=True,
        use_reloader=False
    )
