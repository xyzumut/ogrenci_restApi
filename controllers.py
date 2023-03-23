from flask import Flask,request
from flask_restful import Resource


class MyController(Resource):
    def get(self):
        return {'hello': 'world'}
#Ornek Controller1


class MyController2(Resource):
    def get(self):
        return {'cevap2':'cevap2'}
#Ornek Controller2