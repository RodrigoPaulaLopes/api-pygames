from main import app
from flask import redirect, request, session

@app.before_request
def before_request():
    endpoint = request.endpoint
    rotas_autenticacao = ['login', 'autenticar']
    # Verifique se a rota atual não está nas rotas de autenticação
    if endpoint not in rotas_autenticacao:
        if session['usuario'] and session['usuario'] == None:
            return redirect('login')


