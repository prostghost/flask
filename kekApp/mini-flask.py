from re import template
from urllib import response
from flask import Flask, jsonify, render_template, url_for, request
import requests
from flasgger import Swagger, swag_from
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

#template для swagger'a
template = {
    "swagger":"2.0",
    "info":{
        "title":"API",
        "description":"API for webapp",
        "contact":{
            "email":"example@qq.com",
            "url":"aboba.com"
        },
        "version":"0.0.1"
    },
}

swagger = Swagger(app, template=template)

#Публичные методы для вызова через внешний API
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

#Библиотека для get запросов
todos = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

#Внешний API
API = 'https://api.binance.com/'

#Главная страница
@app.route('/') 
def home():
    print(url_for('home'))
    return render_template('index.html')
    
#Возвращение endpoint1
@app.route('/html/<smth>') 
def html(smth):
    return render_template('page.html', page = url_for('html', smth = smth), endpoint = smth)

#Возвращение endpoint2
@app.route('/page')
def info():
    return render_template('another.html', endpoint = url_for('info'))

#Возвращение endpoint3
@app.route('/profile/<username>') 
def login(username):
    return render_template('page.html', page = url_for('login', username = username), endpoint = username) 

#Возвращение endpoint4
@app.route('/login/<int:id>') 
def user(id):
    return f"ID: <h1>{id}</h1>"

#Для работы со swagger'ом
@app.route('/cuerency/<type>')
@swag_from('./docs/index.yml')
def cuerency(type):
    cuer = {'usd':['64', '65'],
            'eur':['70', '71']}
    if type == 'all':
        result = cuer
    else:
        result = cuer.get(type)

    return jsonify(result)

#Вывод доступных публичных команд для API запроса
@app.route('/binance', methods = ['POST', 'GET'])
def api_requests():
    return render_template('binance.html', endpoint = f'Список доступных команд: {", ".join(methods)}') 
    
#Вывод результата API запроса в виде json
@app.route('/binance_api', methods = ['POST', 'GET'])  
def binance_api():
    req = request.form['api_req']  
    print(req)
    response = requests.get(API + methods[req]['url'])
    return response.json()

#Класс для методов get, put 
class ApiMethods(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

#Добавление ресурса к API 
api.add_resource(ApiMethods, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
    