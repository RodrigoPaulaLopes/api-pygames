from flask import render_template, redirect, request, session
from main import app
from models import Jogos, Usuarios
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