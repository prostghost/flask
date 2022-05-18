from urllib import response
from flask import Flask, render_template, url_for, request
import requests
from flasgger import Swagger
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
swagger = Swagger(api)

methods = {
            # public methods
            'ping':             {'url':'api/v1/ping', 'method': 'GET', 'private': False},
            'time':             {'url':'api/v1/time', 'method': 'GET', 'private': False},
            'exchangeInfo':     {'url':'api/v1/exchangeInfo', 'method': 'GET', 'private': False},
            'depth':            {'url': 'api/v1/depth', 'method': 'GET', 'private': False},
            'trades':           {'url': 'api/v1/trades', 'method': 'GET', 'private': False},
            'historicalTrades': {'url': 'api/v1/historicalTrades', 'method': 'GET', 'private': False},
            'aggTrades':        {'url': 'api/v1/aggTrades', 'method': 'GET', 'private': False},
            'klines':           {'url': 'api/v1/klines', 'method': 'GET', 'private': False},
            'ticker24hr':       {'url': 'api/v1/ticker/24hr', 'method': 'GET', 'private': False},
            'tickerPrice':      {'url': 'api/v3/ticker/price', 'method': 'GET', 'private': False},
            'tickerBookTicker': {'url': 'api/v3/ticker/bookTicker', 'method': 'GET', 'private': False},
            }

todos = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

API = 'https://api.binance.com/'

@app.route('/')
def home():
    print(url_for('home'))
    return render_template('index.html')
    

@app.route('/html/<smth>')
def html(smth):
    return render_template('page.html', page = url_for('html', smth = smth), endpoint = smth)

@app.route('/page')
def info():
    return render_template('another.html', endpoint = url_for('info'))

@app.route('/profile/<username>')
def login(username):
    return render_template('page.html', page = url_for('login', username = username), endpoint = username) 

@app.route('/login/<int:id>')
def user(id):
    return f"ID: <h1>{id}</h1>"


@app.route('/binance', methods = ['POST', 'GET'])
def api_requests():
    return render_template('binance.html', endpoint = f'Список доступных команд: {", ".join(methods)}') 
    

@app.route('/binance_api', methods = ['POST', 'GET'])  
def binance_api():
    req = request.form['api_req']  
    print(req)
    response = requests.get(API + methods[req]['url'])
    return response.json()

class ApiMethods(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(ApiMethods, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
    