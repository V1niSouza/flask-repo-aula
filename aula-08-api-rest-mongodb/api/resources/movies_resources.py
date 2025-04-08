from flask_restful import Resource

from api import api


class MovieList(Resource):
    def get(self):
        return "Olá, mundo! API rodando"

class RecursosAPI(Resource):
    def get(self):
        return "Você enviou uma requisição GET"
    def post(self):
        return "Você enviou uma requisição POST"
    def put(self):
        return "Você enviou uma requisição PUT"
    def delete(self):
        return "Você enviou uma requisição DELETE"
    

    
api.add_resource(MovieList, '/movies')
api.add_resource(RecursosAPI, '/recursos')