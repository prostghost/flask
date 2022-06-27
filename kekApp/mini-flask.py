from msilib import Table
from re import template
from urllib import response
from click import echo
from flask import Flask, jsonify, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import requests
from flasgger import Swagger, swag_from, validate
from flask_restful import Api, Resource
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/api_requests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db = SQLAlchemy(app)


class Requests(db.Model):
    __tablename__ = 'requsets'
    __tableargs__ = {
        'comment': 'Запросы'
    }
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

db.create_all()

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
@app.route('/profile/<username>', methods=['GET'])
@swag_from('./docs/loginGET.yml', methods=['GET']) 
def login(username):
    return render_template('page.html', page = url_for('login', username = username), endpoint = username) 

import json

@app.route('/profile')
@app.route('/profile', methods=['POST'])
@swag_from('./docs/loginPOST.yml', methods=['POST']) 
def profile():
    data = request.data
    dataDict = json.loads(data)
    username = dataDict['username']
    email = dataDict['email']
    password = dataDict['password']

    user =  {
        "username": username,
        "email": email,
        "password": password,
        "userStatus": 0
        }
    
    add_user = Requests(username = username, email = email, password = password)
    db.session.add(add_user)
    db.session.commit()

    return jsonify(user)

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

#Библиотека для get запросов
todos = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

#Класс для методов get, put 
class ApiMethods(Resource):
    @swag_from('./docs/get.yml')
    def get(self, todo_id):
        result = {todo_id: todos[todo_id]}
        return jsonify (result)

    @swag_from('./docs/post.yml')
    def post(self, todo_id):
        todos[todo_id] = {'task': 'new element'}
        result = {todo_id: todos[todo_id]}
        return jsonify (result)

    @swag_from('./docs/put.yml', methods=['PUT'])
    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        result = {todo_id: todos[todo_id]}
        return jsonify (result)

#Добавление ресурса к API 
api.add_resource(ApiMethods, '/<todo_id>')

if __name__ == '__main__':
    app.run(debug=True)  