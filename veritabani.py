import sqlite3

db = sqlite3.connect('ogrenci.db')
imlec = db.cursor()
def tabloOlustur():
    imlec.execute("""CREATE TABLE IF NOT EXISTS ogrenciler (
        id INTEGER PRIMARY KEY NOT NULL, 
        isim VARCHAR(50) NOT NULL, 
        yas INTEGER NOT NULL
    )""")

def ogrenciOlustur(isim, yas):
    imlec.execute("insert into ogrenciler (isim, yas) values(?,?)",(isim, yas))
    db.commit()
    durum = True if imlec.rowcount==1 else False
    return {'durum':durum, 'aciklama':'Kayıt Eklendi' if durum else 'Kayıt eklenmedi'}

def tumOgrencileriGetir():
    imlec.execute("SELECT * FROM ogrenciler")
    rows = imlec.fetchall()
    durum = True if len(rows)>0 else False
    return {'veri':rows, 'durum':durum, 'aciklama':'Kayıtlar getirildi' if durum == True else 'Kayıtlar Bulunamadı'}

def ilgiliOgrenciyiGetir(id):
    imlec.execute("SELECT * FROM ogrenciler WHERE id = ?",(id,))
    rows = imlec.fetchall()
    durum = True if len(rows)>0 else False
    return {'veri':rows, 'durum':durum, 'aciklama':str(id)+'.Kayıt getirildi' if durum == True else str(id)+'.Kayıt Bulunamadı'}

def ilgiliOgrenciyiGuncelle(id= None, isim=None, yas=None):

    sorgu = 'UPDATE ogrenciler SET ' 
    durum = True
    aciklama = ''

    # imlec.rowcount
    if (isim == None and yas == None) or id == None:
        durum = False
        aciklama = 'Parametreler Eksik Gönderildi'
    elif isim == None and yas != None:# isim gelmemiş yaş gelmis
        sorgu += 'yas = ' + str(yas) 
    elif isim != None and yas == None:# isim gelmiş yaş gelmemiş
        sorgu += 'isim = "' + isim + '"'
    else: 
        sorgu +='yas = ' + str(yas) + ', isim = "' + isim + '"'
    
    if durum == True:
        sorgu += ' WHERE id = '+ str(id)
        imlec.execute(sorgu)
        db.commit()
        if imlec.rowcount == 0:
            durum = False
            aciklama = 'İlgili id\'ye Ait Kayıt Bulunamadı'
        else:
            aciklama = str(id)+'.kayıt Güncellendi'
        return {'durum':durum, 'aciklama':aciklama}
    else:
        return {'durum':durum, 'aciklama':aciklama}

def ilgiliOgrenciyiSil(id):
    imlec.execute("DELETE FROM ogrenciler WHERE id = ?",(id,))
    db.commit()
    durum = True if imlec.rowcount == 1 else False
    aciklama = str(id)+'. Kayıt Silindi' if durum else str(id)+'. Kayıt Bulunamadı'
    return {'durum':durum, 'aciklama':aciklama}