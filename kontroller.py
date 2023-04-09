from flask import Flask,request
from flask_restful import Resource

class OgrenciController(Resource):
    def get(self,id=None):
        if id == None :
            return {'sonuc':'Tüm Kayıtlar Listelenecek'}
        else:
            return {'sonuc':str(id)+'. Kayıt Listelenecek'}
    def delete(self,id):
        return {'aciklama':str(id)+'. Kayıt Silinecek'}
    def put(self, id, isim, yas):
        print(isim,yas)
        if isim == 'None':
            isim = None
        if yas == 0:
            yas = None
        print(isim,yas)
        return {'sonuc': str(id)+'. kayıt güncellenecek', 'yas':yas, 'isim':isim}
    def post(self, isim, yas):
        return { 'sonuc':'yeni veri kaydedildi', 'isim':isim, 'yas':yas}
        