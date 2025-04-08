from flask import Flask, render_template
import pymysql.cursors
from controllers import routes
# importanto o model
from models.database import db, Game, Usuario
# importando a biblioteca OS (comandos de S.O)
import os
#importando o PyMySQL
import pymysql


# Criando a instancia do Flask na variável app
app = Flask(__name__, template_folder='views') 

# É como se o arquivo de rota estivesse aq, porem está em outro diretorio, para melhor organização 
routes.init_app(app)

# Define o nome do banco de dados
DB_NAME = 'thegames'
app.config['DATABASE_NAME'] = DB_NAME

# Passando o endereço do banco ao SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost/{DB_NAME}'

# Secret para as flash messages
app.config['SECRET_KEY'] = 'thegamessecret'

# Definir o tempo de sessão
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

# Iniciar o servidor
if __name__ == '__main__':
    # COnecta ao MySQL para criar o banco de dados (se necessário)
    connection = pymysql.connect(host='localhost', user='root', password='', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            #Cria o banco de dados se ele não existir
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
            print(f'O Banco de dados está criado')
    except Exception as e:
        print(f'Erro ao criar o banco de dados: {e}')
    finally:
        connection.close()
        
    # Incializa a aplicação Flask e cria as tabelas do banco
    db.init_app(app=app)
    with app.test_request_context():
        db.create_all()
    
    #Inicia o aplicativo Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
