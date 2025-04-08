from flask import Flask, render_template
from controllers import routes
# importanto o model
from models.database import db, Game, Usuario
# importando a biblioteca OS (comandos de S.O)
import os


# Criando a instancia do Flask na variável app
app = Flask(__name__, template_folder='views') 

# É como se o arquivo de rota estivesse aq, porem está em outro diretorio, para melhor organização 
routes.init_app(app)

# Permite ler o diretorio absoluto de um determinado arquivo
dir = os.path.abspath(os.path.dirname(__file__))

# Passar o diretório do banco ao SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/games.sqlite3')

# Secret para as flash messages
app.config['SECRET_KEY'] = 'thegamessecret'

# Iniciar o servidor
if __name__ == '__main__':
    #Cria o banco de dados quando a aplicação é rodada
    db.init_app(app=app)
    #Esquema de segurança para verificar se o banco já existe
    with app.test_request_context():
        db.create_all()
    app.run(host='localhost', port=5000, debug=True)
