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
class Usuario():
    def __init__(self, id, nome, username, senha):
        self.id = id
        self.nome = nome
        self.username = username
        self.senha = senha

class Jogo():
    def __init__(self, id, name, price, quantity):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price

    def totalValue(self):
        return self.quantity * self.price

usuario1 = Usuario(1, "Rodrigo", "rodrigo@email.com", "123456")
usuario2 = Usuario(2, "matheus", "matheus@email.com", "123456")

usuarios = [usuario1, usuario2]

jogo1 = Jogo(1, "Skyrim", 150, 2)
jogo2 = Jogo(2, "Resident evil", 150, 10)
jogo3 = Jogo(3, "League of legends", 10, 10)

jogos = [jogo1, jogo2, jogo3]

@app.before_request
def before_request():
    endpoint = request.endpoint
    print(endpoint)
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

    return render_template('lista.html', title=title, jogos=jogos)


@app.route("/new", methods=['GET', ])
def form():
    title = 'Cadastrar jogo'
    return render_template('form.html', title=title)


@app.route("/create", methods=['POST', ])
def create():
    data = request.form

    name = str(data.get('name'))
    price = float(data.get('price'))
    quantity = int(data.get('quantity'))

    jogo = Jogo(name, price, quantity)

    jogos.append(jogo)

    return redirect('games')


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/autenticar", methods=['POST'])
def autenticar():
    data = request.form
    for usuario in usuarios:
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
