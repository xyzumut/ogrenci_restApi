from flask import Flask
from flask_restful import Resource, Api
from kontroller import *

app = Flask(__name__)
api = Api(app)

#### Rotalar

api.add_resource(
        OgrenciController, 
        '/ogrenci/getir',# Tüm Kayıtları Getir
        '/ogrenci/getir/<int:id>',# Sadece İlgili Kayıt
        '/ogrenci/ekle/<string:isim>/<int:yas>',# Kayıt Ekle
        '/ogrenci/guncelle/<int:id>/<string:isim>/<int:yas>', #Kayıt Güncelleme
        '/ogrenci/sil/<int:id>',# kayıt sil
    )

#### Rotalar

if __name__ == '__main__':
    app.run(debug=True)