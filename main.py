from flask import Flask
from flask_restful import Resource, Api
from kontroller import *
from rotaFonksiyonu import rota_ekle

app = Flask(__name__)
api = Api(app)

# Yeni Bir Controller / Rota ikilisi ekleneceği zaman controllers.py içerisinde önce controller yapıyı hazırla
# daha sonra aşağıda Rotalar kısmında rota_ekle ile ekle

#### Rotalar

rota_ekle(api, MyController, '/deneme')
rota_ekle(api, MyController2, '/deneme2')

#### Rotalar

if __name__ == '__main__':
    app.run(debug=True)