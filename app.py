from flask import Flask, jsonify, render_template, request, redirect, flash, session, url_for
from flask_session import Session
from .forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__)
app.config["SECRET_KEY"] = "9e4976770668bf1ce6786245c1208161"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:senha@localhost:3306/dbaereo'
db = SQLAlchemy(app)
from .infra.repository.user_repository import UserRepository
from .infra.entities import Aeroporto, Assento, Aviao, Passageiro, Ticket, Usuario, Voo
from .infra.repository.password import verify_password, create_hash_password
with app.app_context():
    db.create_all()
Session(app)

@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    session.clear()
    if request.method == "POST":
        if form.submit_login.data:
            user = str(form.username.data).lower().strip()
            userObj = Usuario.Usuario.query.filter_by(user=user).first()
            senha = str(form.password.data).strip()
            if not userObj or not verify_password(userObj, senha):
                flash("Usuário ou senha inválidos")
                return render_template("index.html", form=form)
            if userObj.user == "root":
                session["name"] = userObj.user
                return redirect("/root")
            #return render_template("próxima página")
        if request.form["submit_button"] == "register":
            return redirect("/register")
    return render_template("index.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        if request.form.get("submit_button") and "login" in request.form["submit_button"]: 
            return redirect("/")
        user = str(form.username.data).lower().strip()
        senha = str(form.password.data).strip()
        confirmar_senha = str(form.confirm_password.data).strip()
        if senha == confirmar_senha:
            tuple = create_hash_password(senha)
            usuario = Usuario.Usuario(user=user, senha=tuple[0], salt=tuple[1])
            db.session.add(usuario)
            db.session.commit()
            flash("Conta criada com sucesso!")
            return render_template("register.html", form=form)
        flash("As senhas precisam ser iguais")
        return render_template("register.html", form=form)
    return render_template("register.html", form=form)

@app.route("/root", methods=["GET", "POST"])
def root():

    if request.method == "POST":
        if "ver" in request.form["submit_button"] or "adicionar" in request.form["submit_button"]:
            session['elemento'] = request.form["submit_button"]
            session['popupDisplay'] = 'block'
            #lista_objects = [item for item in table_repository[request.form["submit_button"].split("_")[1]].select()]
            #lista = [item.__dict__.copy() for item in lista_objects]
            #session['lista'] = lista
            return redirect("/popup")
        if "insert" in request.form["submit_button"]:
            pass
            #titulo = list(request.form.items())[-1][-1].split()[-1].lower()
            #args = []
            #lista_higienizada = list(session.get('lista')[0].keys())
            # abc = []
            #for i in lista_higienizada:
            #    if "instance" not in i and i != "id":
            #        abc.append(i)
            #lista_higienizada = abc
            #for key in lista_higienizada:
            #    args.append(request.form.get(key))
            #table_repository[titulo].insert(*args)
    if session.get("name") == "root":
        #db = DBConnectionHandler()
        #metadata = MetaData()
        #metadata.reflect(bind=db.get_engine())
        #listafoda = list(metadata.tables.keys())
        #tabelaaquiseria = metadata.tables.items()
        #for i in tabelaaquiseria:
        #    print(i)
        #print(listafoda)
        #print(tabelaaquiseria)
        return render_template("root.html")
    return redirect("/")

@app.route("/popup", methods=["GET", "POST"])
def popup():
    flash(str(session.get('elemento')).split("_")[0])
    title = str(session.get('elemento')).split("_")[0].capitalize()
    title += " " + str(session.get('elemento')).split("_")[1].capitalize()
    flash(title)
    return redirect(url_for("root"))

if __name__ == '__main__':
    app.run(debug=True)

