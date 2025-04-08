from flask import Flask, render_template

# Criando a instacia do Flask na variável app
app = Flask(__name__, template_folder='views')  # Representa o nome do arquivo


# Criando rota da aplicação
@app.route('/')
def Home():  # View Function -> função de visualização
    return render_template('index.html')


@app.route('/games')
def Games():
    game = {'Titulo': 'CS-GO',
            'Ano': 2012,
            'Categoria': 'FPS Online'}
    jogadores = ['Rafael', 'Caio', 'Jorge', 'Daniel', 'Maria']
    return render_template('games.html', game=game, jogadores=jogadores)


# Iniciar o servidor
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
