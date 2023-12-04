from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "SECRET"

connector = os.getenv('CONNECTOR')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
database = os.getenv('DATABASE')

app.config['SQLALCHEMY_DATABASE_URI'] = f'{connector}://{user}:{password}@{host}/{database}'

db = SQLAlchemy(app)


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Usuario {self.username}>"


class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


@app.before_request
def before_request():
    endpoint = request.endpoint
    rotas_autenticacao = ['login', 'autenticar']
    # Verifique se a rota atual não está nas rotas de autenticação
    if endpoint not in rotas_autenticacao:
        if session['usuario'] and session['usuario'] == None:
            return redirect('login')


@app.route("/")
def principal():
    return redirect("login")


@app.route('/games')
def findAll():
    title = 'Todos os jogos'
    jogos = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', title=title, jogos=jogos)


@app.route("/new", methods=['GET', ])
def form():
    title = 'Cadastrar jogo'
    return render_template('form.html', title=title)


@app.route("/create", methods=['POST', ])
def create():
    try:
        data = request.form

        name = str(data.get('name'))
        price = float(data.get('price'))
        quantity = int(data.get('quantity'))

        jogo = Jogos.query.filter_by(name=name).first()

        if jogo:
            return redirect('games')

        novo_game = Jogos(name=name, price=price, quantity=quantity)
        db.session.add(novo_game)
        db.session.commit()

        return redirect('games')
    except Exception as e:
        print(e)
    finally:
        pass


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/autenticar", methods=['POST'])
def autenticar():
    data = request.form
    usuario = Usuarios.query.filter_by(username=data.get('email')).first()
    if data.get('email') == usuario.username and data.get('senha') == usuario.senha:
        session['usuario'] = usuario.nome
        return redirect("games")
    else:
        return redirect("login")


@app.route("/logout")
def logout():
    session['usuario'] = None
    return redirect('login')


if __name__ == '__main__':
    app.run(debug=True)
