from flask import render_template, request, redirect, url_for, flash, session
# Importando o Model
from models.database import db, Game, Usuario
# Essa bibilioteca serve para ler uma determinada url
import urllib
# Converte os dados para um formato json
import json
# importando biblioteca para hash de senha
from werkzeug.security import generate_password_hash, check_password_hash
# Biblioteca para editar FLash message
from markupsafe import Markup # Inclui HTML dentro das Flash Messages

jogadores = []

gamelist =[{'titulo': 'CS-GO',
        'ano': 2012,
        'categoria': 'FPS Online'}]

# 
def init_app(app):
    # Função de middleware para verificar a autenticação do usuário
    @app.before_request
    def check_auth():
        # Rotas que não precisam de autenticação
        routes = ['login', 'caduser', 'Home']
        
        # Se a rota atual não requer autenticação, permite o acesso
        if request.endpoint in routes or request.path.startswith('/static/'):
            return
        
        # Se o usuario não estiver antenticado, redireciona para a página de login
        if 'user_id' not in session:
            return redirect(url_for('login'))
    
    # Criando rota da aplicação
    @app.route('/')
    def Home():  # View Function -> função de visualização
        return render_template('index.html')
    
    @app.route('/games', methods=['GET', 'POST'])
    def games():
        game = gamelist[0] 
        if request.method == 'POST':
            if request.form.get('jogador'):
                jogadores.append(request.form.get('jogador'))
                return redirect(url_for('games'))
                
        return render_template('games.html', game=game, jogadores=jogadores)

    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            form_data = request.form.to_dict()
            gamelist.append(form_data)
            return(redirect(url_for('cadgames')))
        return render_template('cadgames.html', gamelist=gamelist)
   
    @app.route('/apigames', methods=['GET', 'POST'])
    # Passando parametros para a rota
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    # Definindo que o parametro é opcional
    def apigames(id=None):
        url = 'https://www.freetogame.com/api/games'
        res = urllib.request.urlopen(url)
        data = res.read()
        gamesjson = json.loads(data)
        
        if id:
            ginfo = []
            for g in gamesjson:
                if g['id'] == id:
                    ginfo=g
                    break
            if ginfo:
                return render_template('gameinfo.html', ginfo=ginfo)
            else:
                return f'Game com a ID {id} não foi encontrado.'
        return render_template('apigames.html', gamesjson=gamesjson)
    
    #Rota com o CRUD de JOGOS
    @app.route('/estoque')
    def estoque():
        # Método do SQLAchemy que faz um select no banco na tabela Games
        gamesestoque = Game.query.all()
        return render_template('estoque.html', gamesestoque=gamesestoque)

    #Rota de Login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            
            # Buscando o usuário no banco
            user = Usuario.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['email'] = user.email
                nickname = user.email.split('@')
                flash(f'login bem-sucedido! Bem-Vindo {nickname[0]}!', 'success')
                return redirect(url_for('Home'))
            else:
                flash('Falha login. Verifique seu nome de usuario e senha.', 'danger')
        return render_template('login.html')
    
    # Rota de LOGOUT
    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        #Destruindo a sessão do usuário
        session.clear()
        return redirect(url_for('Home'))
    
    
    #Rota de Cadastro       
    @app.route('/caduser', methods=['GET', 'POST'])
    def caduser():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            
            # Verificando se o usuário já existe
            user = Usuario.query.filter_by(email=email).first()
            # Se o usuário existir
            if user:
                msg = Markup("Usuário já cadastrado. Faça <a href='/login'>login</a>")
                flash(msg, 'danger')
                return redirect(url_for('caduser'))
            # Caso o usuário exista
            else: 
                # Gerando o hash
                hashed_password = generate_password_hash(password, method='scrypt')
                new_user = Usuario(email=email, password=hashed_password) 
                db.session.add(new_user)
                db.session.commit()
                
                # Mensagem de sucesso após o cadastro
                flash('Registro realizado com sucesso! Faça o login', 'success')
                #Redirecionando para a página de login
                return redirect(url_for('login'))
        return render_template('caduser.html')