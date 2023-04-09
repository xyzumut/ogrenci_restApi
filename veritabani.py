import sqlite3
import os

db = sqlite3.connect('ogrenci.db', check_same_thread=False)
imlec = db.cursor()

def tabloOlustur():
    imlec.execute("""CREATE TABLE IF NOT EXISTS ogrenciler (
        id INTEGER PRIMARY KEY NOT NULL, 
        isim VARCHAR(50) NOT NULL, 
        yas INTEGER NOT NULL,
        resim VARCHAR(1000)
    )""")

def ogrenciOlustur(isim, yas, resim = None):
    if yas > 0 :
        if resim != None:
            imlec.execute("insert into ogrenciler (isim, yas, resim) values(?,?, ?)",(isim, yas, resim))
        else:
            imlec.execute("insert into ogrenciler (isim, yas) values(?,?)",(isim, yas))
        db.commit()
        durum = True if imlec.rowcount==1 else False
        return {'durum':durum, 'aciklama':'Kayıt Eklendi' if durum else 'Kayıt eklenmedi'}
    else:
        return {'durum':False, 'aciklama':'Kimse 0 yaşında değildir'}


def tumOgrencileriGetir():
    imlec.execute("SELECT * FROM ogrenciler")
    rows = imlec.fetchall()
    durum = True if len(rows)>0 else False
    veri = []
    for i in range(len(rows)):
        veri.append({'id':rows[i][0], 'isim':rows[i][1], 'yas':rows[i][2], 'resim':rows[i][3] if rows[i][3] != None else 'Resim yok'})
    return {'veri':veri, 'durum':durum, 'aciklama':'Kayıtlar getirildi' if durum == True else 'Kayıtlar Bulunamadı'}

def ilgiliOgrenciyiGetir(id):
    imlec.execute("SELECT * FROM ogrenciler WHERE id = ?",(id,))
    rows = imlec.fetchall()
    durum = True if len(rows)>0 else False
    return {'veri':rows, 'durum':durum, 'aciklama':str(id)+'.Kayıt getirildi' if durum == True else str(id)+'.Kayıt Bulunamadı'}

def ilgiliOgrenciyiGuncelle(id, yeniIsim=None, yeniYas=None, yeniResim=None):
    aciklama = 'Güncelleme Başarılı'
    durum = True
    eskiOgrenci = ilgiliOgrenciyiGetir(id)

    if eskiOgrenci['durum'] == False:
        aciklama = str(id)+'. kayıt bulunamadı'
        durum = False
    else:

        eskiIsim = eskiOgrenci['veri'][0][1]
        eskiYas = eskiOgrenci['veri'][0][2]
        eskiResim = eskiOgrenci['veri'][0][3]
        
        isim = yeniIsim if yeniIsim!=None else eskiIsim
        yas = yeniYas if yeniYas!=None else eskiYas


        if yeniResim!=None: # Güncellemek İçin Yeni Resim Göndermişiz Demektir

            uzanti = yeniResim.filename.split('.')[-1]
            yeniResim.filename = str(isim).replace(' ','')+ str(yas) +'.'+ uzanti

            if eskiResim == None: # eski Resim nulldur o yüzden direkt güncelleme yapıp resmi kaydedelim
                yeniResim.save(os.path.join('uploads', yeniResim.filename)) 
                imlec.execute("UPDATE ogrenciler SET isim = ?, yas = ?, resim = ? WHERE id = ?",(isim, yas, yeniResim.filename, id))

            else: # eski resim mevcuttur, eski resmi silip yenisini dosyaya yaz + veritabanında güncelleme yap
                os.remove('uploads/'+eskiResim)
                yeniResim.save(os.path.join('uploads', yeniResim.filename)) 
                imlec.execute("UPDATE ogrenciler SET isim = ?, yas = ?, resim = ? WHERE id = ?",(isim, yas, yeniResim.filename, id))
        else: # Yeni resim göndermemişizdir sadece isim ve yaşı updatele
            imlec.execute("UPDATE ogrenciler SET isim = ?, yas = ? WHERE id = ?",(isim, yas, id))
        
        db.commit()
    return {'durum':durum, 'aciklama':aciklama}

def ilgiliOgrenciyiSil(id):
    """
    durum = true için işlem tamam
    durum = false için ilgili id'de kayıt bulunamaz
    resim = None değilse resim vardır ve bu resmin yolu döner, resim silinmelidir
    [Örnek:{'durum': True, 'aciklama': '3. Kayıt Silindi', 'resim': 'uploads/ahmet31.PNG'}]
    """
    imlec.execute("SELECT resim FROM ogrenciler WHERE id = ?",(id,))
    rows = imlec.fetchall()
    resim = None
    if len(rows) > 0 and rows[0][0]!=None : resim = str(rows[0][0])
    imlec.execute("DELETE FROM ogrenciler WHERE id = ?",(id,))
    db.commit()
    durum = True if imlec.rowcount == 1 else False
    aciklama = str(id)+'. Kayıt Silindi' if durum else str(id)+'. Kayıt Bulunamadı'
    return {'durum':durum, 'aciklama':aciklama, 'resim':resim}

"""
öğrenci ekleme full okey
çoklu listeleme okey
tekli listeleme okey
silme okey
guncelleme okey
"""