from flask import Flask,request, send_file
from flask_restful import Resource
import os
from veritabani import *
class DenemeController(Resource):
    def post(self):
        if 'resim' in request.files:
            print(request.files['resim'].filename.split('.')[-1])
        else :
            print('yok')
        pass
        # resim = request.files['resim']
        # resim.save(os.path.join('uploads', resim.filename))     
class ResimController(Resource):
    def get(self,resim):
        tabloOlustur()
        return send_file('uploads/'+resim)

class OgrenciController(Resource):
    def get(self,id=None):
        tabloOlustur()
        if id == None :
            response = tumOgrencileriGetir()
            apiResponse = {}
            apiResponse['aciklama'] = response['aciklama']
            
            if response['durum'] == True:
                for i in range(len(response['veri'])):
                    if response['veri'][i]['resim'] != None:
                        resim = response['veri'][i]['resim']
                        response['veri'][i]['resim'] = 'http://127.0.0.1:5000/resim/'+resim if resim !='Resim yok' else resim
            return response
        else:
            response = ilgiliOgrenciyiGetir(id)
            apiResponse = {}
            apiResponse['aciklama'] = response['aciklama']
            if response['durum'] != False:
                kayit_id = response['veri'][0][0]
                isim = response['veri'][0][1]
                yas = response['veri'][0][2]
                resim = response['veri'][0][3]
                apiResponse['id'] = kayit_id
                apiResponse['isim'] = isim
                apiResponse['yas'] = yas
                apiResponse['resim'] = 'Resim Yok'
                if resim != None:
                    apiResponse['resim']='http://127.0.0.1:5000/resim/'+resim
            return apiResponse
        
    def delete(self,id):
        tabloOlustur()
        response = ilgiliOgrenciyiSil(id)
        if response['resim'] != None : os.remove('uploads/'+response['resim'])
        return {'durum':response['durum'], 'aciklama':response['aciklama']}

    def put(self, id, isim, yas):
        tabloOlustur()
        yeniIsim = isim if isim != 'bos' else None
        yeniYas = yas if yas != 0 else None
        if 'resim' in request.files:
            yeniResim = request.files['resim']
        else:
            yeniResim = None
            
        response = ilgiliOgrenciyiGuncelle(id, yeniIsim, yeniYas, yeniResim)

        return response 
    

    def post(self, isim, yas):
        tabloOlustur()
        response = None
        if 'resim' in request.files: #resim var ise 
            resim = request.files['resim']
            uzanti = resim.filename.split('.')[-1]
            resim.filename = str(isim).replace(' ','')+ str(yas) +'.'+ uzanti
            resim.save(os.path.join('uploads', resim.filename)) 
            response = ogrenciOlustur(isim=isim, yas=yas, resim=resim.filename)
        else:
            response = ogrenciOlustur(isim=isim, yas=yas)
        return response
