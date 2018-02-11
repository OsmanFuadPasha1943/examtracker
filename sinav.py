#!/bin/python

class Ders:
    def __init__(self, ders_adi, toplam, dogru, yanlis):
        self.ders_adi = ders_adi
        self.toplam = toplam
        self.dogru = dogru
        self.yanlis = yanlis
        self.bos = self.toplam - (self.dogru + self.yanlis)
        self.net = self.calculate_net(self.dogru, self.yanlis)
    
    def __repr__(self):
        # Turkce{toplam=20, dogru=18, yanlis=2, bos=0, net=17.5}
        return  self.ders_adi + "{" + \
                "T: " + str(self.toplam) + ", " + \
                "D: " + str(self.dogru) + ", " + \
                "Y: " + str(self.yanlis) + ", " + \
                "B: " + str(self.bos) + ", " + \
                "N: " + str(self.net) + "}"
    
    def calculate_net(self, dogru, yanlis):
        net = dogru - (yanlis * 0.25)
        return net

class Sinav:
    def __init__(self, dersler, tarih, mekan, yayinevi):
        self.dersler = dersler
        self.tarih = tarih
        self.mekan = mekan
        self.yayinevi = yayinevi
    
    def get_results(self):
        butun_toplam = 0
        butun_dogru =  0
        butun_yanlis = 0
        butun_bos = 0
        butun_net = 0
        for ders in self.dersler:
            butun_toplam += ders.toplam
            butun_dogru += ders.dogru
            butun_yanlis += ders.yanlis
            butun_bos += ders.bos
            butun_net += ders.net
        
        return {
            "B_T": butun_toplam,
            "B_D": butun_dogru,
            "B_Y": butun_yanlis,
            "B_N": butun_net,
            "B_B": butun_bos
            }
            
    def __repr__(self):
        return  self.tarih + "{" + \
                "mekan: " + self.mekan + ", " + \
                "yayinevi: " + self.yayinevi + "}"
                
                
class CsvParser:
    def __init__(self, filename, has_header=False):
        self.has_header = has_header
        self.flnm = filename
        self.header = None

    def parse(self):
        data = self.readfile()
        lines = self.getlines(data)
        return self.create_sinavlar(lines)
        
    def readfile(self):
        fh = open(self.flnm)
        data = fh.read()
        fh.close()
        return data
        
    def getlines(self, content):
        lines = content.split("\n")
        if self.has_header:
            self.header = lines[0]
            lines = lines[1:]
        return lines
            
    def create_sinavlar(self, lines):
        lines = lines[0: len(lines) - 1]
        sinavlar = []
        for line in lines:
            values = line.split("; ")
            #print(values)
            # TARIH; MEKAN; YAYINEVI; DERSIN_ADI, TOPLAM, DOGRU, YANLIS;
            sinav_dersleri = values[3:]
            dersler = self.extract_dersler(sinav_dersleri)
            sinav = Sinav(
                dersler=dersler,
                tarih=values[0],
                mekan=values[1],
                yayinevi=values[2]
                )
            sinavlar.append(sinav)
        return sinavlar
        
    def extract_dersler(self, ders_bilgileri):
        dersler = []
        for ders_bilgisi in ders_bilgileri:
            bilgiler = ders_bilgisi.split(", ")
            ders = Ders(
                ders_adi=bilgiler[0],
                toplam=int(bilgiler[1]),
                dogru=int(bilgiler[2]),
                yanlis=int(bilgiler[3])
                )
            dersler.append(ders)
        return dersler
        
def show_menu():
    menu = """
    1 - Sinav Ekle
    2 - Sinav Goster
    3 - Tum Sinavlari Goster
    4 - Sinav Listesi
    0 - Cikis
    """
    print(menu)
    

"""
  herhangi bir input almayacak
  output olarak da bir tane Sinav objesi donderecek
  Sinav objesini olusturmak icin gerekli bilgiler kullanicidan alinacak
"""

def create_sinav():
    tarih = input("Sınava girdiğiniz tarih: ")
    mekan = input("Sınava girdiğiniz yer: ")
    yayin = input("Sınav yayını: ")
    derslerin_adi = ["turkce", "matematik", "fen", "sosyal"]
    dersler = []
    for ders_adi in derslerin_adi:
        dersler.append(create_ders(ders_adi))
    # [create_ders(d_a for d_a in derslerin_adi]
    x = Sinav(dersler, mekan=mekan, tarih=tarih, yayinevi=yayin)
    return x
    
"""
  input dersin adi olacak
  output olarak bir tane Ders objesi donecek
  Ders objesi icin gerekli bilgiler kullanicidan alinacak
"""
def create_ders(ders_adi):
    print(ders_adi + " dersinin bilgileri girilecektir.")
    toplam_soru = int(input("Toplam soru sayısını giriniz: "))
    dogru_soru = int(input("Toplam doğru sayısını giriniz: "))
    yanlis_soru = int(input("Toplam yanlış sayısını giriniz: "))
    new_ders = Ders(ders_adi, toplam_soru, dogru_soru, yanlis_soru)
    return new_ders
    
"""
  verilen sinavlar listesini sinavlar.csv dosyasina yazdiracak
"""

def overwrite_csv_file(sinav_listesi):
    # sinav = sinav_listesi[0]
    header = "TARIH; MEKAN; YAYINEVI; DERSIN_ADI, TOPLAM, DOGRU, YANLIS; DERSIN_ADI, TOPLAM, DOGRU, YANLIS; DERSIN_ADI, TOPLAM, DOGRU, YANLIS; DERSIN_ADI, TOPLAM, DOGRU, YANLIS;"
    sinav_format = "%s; %s; %s; %s; %s; %s; %s\n"
    
    fh = open("sinavlar.csv", "w")
    fh.write(header + "\n")
    for sinav in sinav_listesi:
        ders_formatlari = format_dersler(sinav.dersler)
        sinav_str = sinav_format % (
            sinav.tarih, sinav.mekan, sinav.yayinevi,
            ders_formatlari[0], ders_formatlari[1], ders_formatlari[2], ders_formatlari[3])
        fh.write(sinav_str)
    
    fh.close()
    
def format_dersler(dersler):
    #  DERSIN_ADI, TOPLAM, DOGRU, YANLIS
    ders_format = "%s, %d, %d, %d"
    ders_formatlari = []
    for ders in dersler:
        ders_formatlari.append(ders_format % (ders.ders_adi, ders.toplam, ders.dogru, ders.yanlis))
    return ders_formatlari
    
    
#turkce = Ders(ders_adi="Turkce", dogru=27, toplam=40, yanlis=8)
#math = Ders(ders_adi="Matematik", dogru=15, toplam=40, yanlis=2)
#fen = Ders(ders_adi="Fen", dogru=11, toplam=20, yanlis=6)
#sosyal = Ders(ders_adi="Sosyal", dogru=13, toplam=20, yanlis=1)

#print(turkce)

#dersler = [turkce, math, sosyal, fen]

#sinavx = Sinav(dersler, "01-12-2017", "Okul", "Birey")

#sonuclar = sinavx.get_results()
#print(sonuclar)

#sinavlar = [sinavx]

my_parser = CsvParser("sinavlar.csv", has_header=True)

sinavlar = my_parser.parse()

secim = 1


while secim != 0:
    show_menu()
    secim = int(input('Seciminiz: '))
    print(secim)
    if secim == 4:
        for sinav in sinavlar:
            print(sinav)
    elif secim == 3:
        for sinav in sinavlar:
            print(sinav.get_results())
    elif secim == 2:
        secilen_sinav = sinavlar[0]
        print(secilen_sinav)
        print(secilen_sinav.get_results())
    elif secim == 1:
        new_sinav = create_sinav()
        print("Sınavınız eklendi.")
        print(new_sinav)
        sinavlar.append(new_sinav)
        

overwrite_csv_file(sinavlar)
print("Dataniz basariyla sinavlar.csv dosyasina yazdirildi.")
print('Cikis yaptiniz')




























