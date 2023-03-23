from flask import Flask
from flask_restful import Resource, Api
from controllers import *
from route import rota_ekle

app = Flask(__name__)
api = Api(app)

#### Rotalar

rota_ekle(api, MyController, '/deneme')
rota_ekle(api, MyController2, '/deneme2')

#### Rotalar

if __name__ == '__main__':
    app.run(debug=True)