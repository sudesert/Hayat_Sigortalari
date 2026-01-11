import pandas as pd

# =============================================================================
# BÖLÜM 1: AYARLAR VE VERİ YÜKLEME (Global Alan)
# =============================================================================

# 1. ADIM: Tabloyu içe aktar
# Dosya yolunu kendi bilgisayarına göre güncelle
dosya_yolu = ("TRSH2010_Erkek.csv")

# Hem ayırıcıyı (sep) hem de ondalık işaretini (decimal) belirtiyoruz
df = pd.read_csv(dosya_yolu, sep=';', decimal=',', encoding='latin1')

# Sütun isimlerindeki olası hataları (büyük harf, boşluk) temizliyoruz
df.columns = df.columns.str.strip().str.lower()

# 2. ADIM: Komütasyon sütunlarını hesaplayan fonksiyon
def komutasyon_hazirla(faiz_orani):
    # İskonto faktörü (v)
    v = 1 / (1 + faiz_orani)
    
    # --- HATAYI ÇÖZEN KRİTİK EKLEME ---
    # Sütunları zorla sayı tipine (float) çeviriyoruz, hata verenleri temizliyoruz
    df['lx'] = pd.to_numeric(df['lx'], errors='coerce')
    df['yas'] = pd.to_numeric(df['yas'], errors='coerce')
    df['dx'] = pd.to_numeric(df['dx'], errors='coerce')
    
    # Yaşam sütunları (Dx, Nx, Sx)
    df['Dx'] = df['lx'] * (v ** df['yas'])
    df['Nx'] = df['Dx'][::-1].cumsum()[::-1]
    df['Sx'] = df['Nx'][::-1].cumsum()[::-1]
    
    # Ölüm sütunları (Cx, Mx, Rx)
    df['Cx'] = df['dx'] * (v ** (df['yas'] + 1))
    df['Mx'] = df['Cx'][::-1].cumsum()[::-1]
    df['Rx'] = df['Mx'][::-1].cumsum()[::-1]

# =============================================================================
# BÖLÜM 2: HESAPLAMA FONKSİYONLARI (Kütüphane Kısmı)
# =============================================================================



#---------------------------------------------------------
#TEK ÖDEMELİ YAŞAM SİGORTASI (töys)
#---------------------------------------------------------
# 1. prim bulma

def toys_prim_hesapla(yas, sure, teminat):
    #Dx: sigortaya girdiği yaşı
    #Dx_n: teminatı alacağı yaşı
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    Dx_n = df.loc[df['yas'] == yas + sure, 'Dx'].values[0]
    
    ntp = (Dx_n / Dx) * teminat  #ntp=net tek prim
    return round(ntp, 4) #virgülden sonra 4 basamak alıyoruz.


# 2. teminat bulma

def toys_teminat_hesapla(yas, sure, prim):
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    Dx_n = df.loc[df['yas'] == yas + sure, 'Dx'].values[0]
    
    teminat = (prim * Dx) / Dx_n
    return round(teminat, 4) 



#---------------------------------------------------------
#ÖMÜR BOYU ÖDEMELİ YAŞAM  SİGORTASI (öböys)
#---------------------------------------------------------
# 1. prim bulma

#dönem başı

def oboys_prim_hesaplama1(yas, teminat):
    Nx = df.loc[df['yas'] == yas, 'Nx'].values[0]
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    
    ntp = (Nx / Dx) * teminat  #ntp=net tek prim
    return round(ntp, 4)
    

#dönem sonu

def oboys_prim_hesaplama2(yas, teminat):
    Nx_arti_1 = df.loc[df['yas'] == (yas + 1), 'Nx'].values[0]
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    
    ntp = (Nx_arti_1 / Dx) * teminat  #ntp=net tek prim
    return round(ntp, 4)
    

# 2. teminat bulma

#dönem başı

def oboys_teminat_hesaplama1(yas, prim):
    Nx = df.loc[df['yas'] == yas, 'Nx'].values[0]
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    
    # teminat = (prim * Dx) / Nx
    teminat = (prim * Dx) / Nx
    return round(teminat, 4)


#dönem sonu 

def oboys_teminat_hesaplama2(yas, prim):
    Nx_arti_1 = df.loc[df['yas'] == (yas + 1), 'Nx'].values[0]
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    
    # teminat = (prim * Dx) / Nx+1
    teminat = (prim * Dx) / Nx_arti_1
    return round(teminat, 4)



#---------------------------------------------------------
#DÖNEMSEL YAŞAM SİGORTASI (dys)
#---------------------------------------------------------
# 1. prim bulma

#dönem başı
def dys_prim_hesaplama1(yas, sure, teminat):
    Nx = df.loc[df['yas'] == yas, 'Nx'].values[0]
    Nx_n = df.loc[df['yas'] == yas + sure, 'Nx'].values[0]
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    
    # ntp = ((Nx - Nx+n) / Dx) * teminat
    ntp = ((Nx - Nx_n) / Dx) * teminat
    return round(ntp, 4)


# dönem sonu
def dys_prim_hesaplama2(yas, sure, teminat):
    Nx_arti_1 = df.loc[df['yas'] == (yas + 1), 'Nx'].values[0]
    Nx_n_arti_1 = df.loc[df['yas'] == (yas + sure + 1), 'Nx'].values[0]
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    
    # ntp = ((Nx+1 - Nx+n+1) / Dx) * teminat
    ntp = ((Nx_arti_1 - Nx_n_arti_1) / Dx) * teminat
    return round(ntp, 4)


# 2. teminat bulma

# dönem başı
def dys_teminat_hesaplama1(yas, sure, prim):
    Nx = df.loc[df['yas'] == yas, 'Nx'].values[0]
    Nx_n = df.loc[df['yas'] == yas + sure, 'Nx'].values[0]
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    
    # teminat = (prim * Dx) / (Nx - Nx_n)
    teminat = (prim * Dx) / (Nx - Nx_n)
    return round(teminat, 4)



# dönem sonu
def dys_teminat_hesaplama2(yas, sure, prim):
    Nx_arti_1 = df.loc[df['yas'] == (yas + 1), 'Nx'].values[0]
    Nx_n_arti_1 = df.loc[df['yas'] == (yas + sure + 1), 'Nx'].values[0]
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    
    # teminat = (prim * Dx) / (Nx_arti_1 - Nx_n_arti_1)
    teminat = (prim * Dx) / (Nx_arti_1 - Nx_n_arti_1)
    return round(teminat, 4)



#---------------------------------------------------------
#ERTELENMİŞ YAŞAM SİGORTASI (eys)
#---------------------------------------------------------
# 1. prim bulma

#dönem başı (ödemeler r yıl sonra başlayacak)
def eys_prim_hesaplama1(yas, r, teminat): #r ertelenme süresi
    # Nx+r: Ödemelerin başladığı yaşın komütasyon değeri
    Nx_r = df.loc[df['yas'] == yas + r, 'Nx'].values[0]
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    
    # ntp = (Nx+r / Dx) * teminat
    ntp = (Nx_r / Dx) * teminat
    return round(ntp, 4)


#dönem sonu (Ödemeler m+1 yıl sonra başlar)
def eys_prim_hesaplama2(yas, r, teminat):
    Nx_r_arti_1 = df.loc[df['yas'] == (yas + r + 1), 'Nx'].values[0]
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    
    # ntp = (Nx+r+1 / Dx) * teminat
    ntp = (Nx_r_arti_1 / Dx) * teminat
    return round(ntp, 4)


# 2. teminat bulma

# dönem başı
def eys_teminat_hesaplama1(yas, r, prim):
    Nx_r = df.loc[df['yas'] == yas + r, 'Nx'].values[0]
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    
    # teminat = (prim * Dx) / Nx+r
    teminat = (prim * Dx) / Nx_r
    return round(teminat, 4)


# dönem sonu teminat bulma
def eys_teminat_hesaplama2(yas, r, prim):
    # Nx+r+1: Erteleme süresi bittikten 1 yıl sonraki komütasyon değeri
    Nx_r_arti_1 = df.loc[df['yas'] == (yas + r + 1), 'Nx'].values[0]
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    
    # teminat = (prim * Dx) / Nx+m+1
    teminat = (prim * Dx) / Nx_r_arti_1
    return round(teminat, 4)



#---------------------------------------------------------
#DÖNEMSEL VE ERTELENMİŞ YAŞAM SİGORTASI (dveys)
#---------------------------------------------------------
# 1. prim bulma

#dönem başı
def dveys_prim_hesaplama1(yas, r, sure, teminat):
    Nx_r = df.loc[df['yas'] == yas + r, 'Nx'].values[0]
    Nx_r_n = df.loc[df['yas'] == yas + r + sure, 'Nx'].values[0]
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    
    # ntp = ((Nx+r - Nx+r+n) / Dx) * teminat
    ntp = ((Nx_r - Nx_r_n) / Dx) * teminat
    return round(ntp, 4)

#dönem sonu
def dveys_prim_hesaplama2(yas, r, sure, teminat):
    Nx_r_1 = df.loc[df['yas'] == yas + r + 1, 'Nx'].values[0]
    Nx_r_n_1 = df.loc[df['yas'] == yas + r + sure + 1, 'Nx'].values[0]
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    
    # ntp = ((Nx+r+1 - Nx+r+n+1) / Dx) * teminat
    ntp = ((Nx_r_1 - Nx_r_n_1) / Dx) * teminat
    return round(ntp, 4)


# 2. teminat bulma

#dönem başı
def dveys_teminat_hesaplama1(yas, r, sure, prim):
    Nx_r = df.loc[df['yas'] == yas + r, 'Nx'].values[0]
    Nx_r_n = df.loc[df['yas'] == yas + r + sure, 'Nx'].values[0]
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    
    # teminat = (prim * Dx) / (Nx_r - Nx_r_n)
    teminat = (prim * Dx) / (Nx_r - Nx_r_n)
    return round(teminat, 4)


#dönem sonu
def dveys_teminat_hesaplama2(yas, r, sure, prim):
    Nx_r_1 = df.loc[df['yas'] == yas + r + 1, 'Nx'].values[0]
    Nx_r_n_1 = df.loc[df['yas'] == yas + r + sure + 1, 'Nx'].values[0]
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    
    # teminat = (prim * Dx) / (Nx+r+1 - Nx+r+n+1)
    teminat = (prim * Dx) / (Nx_r_1 - Nx_r_n_1)
    return round(teminat, 4)



#---------------------------------------------------------
#ARİTMETİK DEĞİŞKEN ÖDEMELİ YAŞAM SİGORTASI (adoys)
#---------------------------------------------------------
# i. ÖMÜR BOYU ÖDEMELİ
# 1. prim bulma
import math

def adoys_omur_boyu_prim(yas, baslangic_teminat, degisim_miktari):

    #Bu fonksiyon şuna bakar:
    #1. Eğer ARTAN veya SABİT ise: Klasik Ömür Boyu formülünü (sonsuz) kullanır.
    #2. Eğer AZALAN ise: Paranın kaç yılda sıfırlanacağını bulur ve o süre kadar hesaplar.
    
    
    # SENARYO 1: AZALAN SİGORTA (degisim_miktari NEGATİF)
    if degisim_miktari < 0:
        # Paranın kaç yıl yeteceğini bulalım (Örn: 10000 / 1000 = 10 yıl)
        # abs() mutlak değer alır (-1000'i 1000 yapar)
        bitecek_yil = math.floor(baslangic_teminat / abs(degisim_miktari))
        
        print(f"BİLGİ: Bu azalan sigorta {bitecek_yil} yıl sonra sıfırlanacaktır.")
        print(f"Hesaplama {bitecek_yil} yıllık 'Süreli Sigorta' olarak yapılıyor...")
        
        # Buradan sonra "Süreli Azalan Sigorta" formülü devreye girer
        # Daha önce yazdığımız süreli mantığın aynısı:
        Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
        Nx = df.loc[df['yas'] == yas, 'Nx'].values[0]
        Sx = df.loc[df['yas'] == yas, 'Sx'].values[0]
        
        Nx_n = df.loc[df['yas'] == yas + bitecek_yil, 'Nx'].values[0]
        Sx_n = df.loc[df['yas'] == yas + bitecek_yil, 'Sx'].values[0]
        
        # Süreli Formülümüz:
        # (P + d) * (Nx - Nx_n)
        sanal_sabit = baslangic_teminat + abs(degisim_miktari) # P + d mantığı
        sabit_kisim = ((Nx - Nx_n) / Dx) * sanal_sabit
        
        # - d * (Sx - Sx_n - n*Nx_n)
        artan_kisim = ((Sx - Sx_n - (bitecek_yil * Nx_n)) / Dx) * abs(degisim_miktari)
        
        # Azalan olduğu için ÇIKARIYORUZ
        toplam_ntp = sabit_kisim - artan_kisim
        return round(toplam_ntp, 4)

    # SENARYO 2: ARTAN VEYA SABİT SİGORTA (POZİTİF veya 0)
    else:
        # Standart Ömür Boyu Formülü
        Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
        Nx = df.loc[df['yas'] == yas, 'Nx'].values[0]
        Sx = df.loc[df['yas'] == yas, 'Sx'].values[0]
        
        # (P - d) * Nx/Dx
        sabit_kisim = (Nx / Dx) * (baslangic_teminat - degisim_miktari)
        
        # + d * Sx/Dx
        degisken_kisim = (Sx / Dx) * degisim_miktari
        
        toplam_ntp = sabit_kisim + degisken_kisim
        return round(toplam_ntp, 4)

# 2. teminat bulma
def adoys_omurboyu_teminat(yas, prim, degisim_miktari):
    """
    Ömür boyu maaş başlangıcını bulur.
    UYARI: Azalan miktar kabul etmez.
    """
    
    # --- GÜVENLİK KONTROLÜ (YENİ EKLENDİ) ---
    # Ömür boyu sigortada maaş azalamaz, çünkü elbet bir gün biter.
    if degisim_miktari < 0:
        return "HATA: 'Ömür Boyu' sigortada azalan maaş hesaplanamaz. Lütfen 'Dönemsel' fonksiyonu kullanın."

    # Standart Hesaplama (Sadece Artan ve Sabit İçin)
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    Nx = df.loc[df['yas'] == yas, 'Nx'].values[0]
    Sx = df.loc[df['yas'] == yas, 'Sx'].values[0]

    katsayi_sabit = Nx / Dx
    katsayi_artan = Sx / Dx

    baslangic_teminati = (prim - (degisim_miktari * katsayi_artan)) / katsayi_sabit + degisim_miktari
    
    return round(baslangic_teminati, 2)

# ii. DÖNEMSEL ÖDEMELİ
# 1. prim bulma
def adoys_donemsel_prim(yas, sure, baslangic_teminat, degisim_miktari):

    #TEK FORMÜL - TÜM SENARYOLAR:
    #1. Artan Sigorta İçin: degisim_miktari'nı POZİTİF girin. (Örn: 1000)
    #2. Azalan Sigorta İçin: degisim_miktari'nı NEGATİF girin. (Örn: -1000)
    #3. Sabit Sigorta İçin: degisim_miktari'nı 0 (SIFIR) girin.
    

    # GÜVENLİK KONTROLÜ (Sadece Azalan Sigorta İçin)
    # Eğer değişim eksi ise, maaşın sıfırın altına düşüp düşmediğini kontrol et.
    if degisim_miktari < 0:
        son_odeme = baslangic_teminat + ((sure - 1) * degisim_miktari)
        if son_odeme < 0:
            return f"HATA: Bu hızla azalırsa {sure}. yılda maaş eksiye düşer! ({son_odeme})"

    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    Nx = df.loc[df['yas'] == yas, 'Nx'].values[0]
    Sx = df.loc[df['yas'] == yas, 'Sx'].values[0]
    
    # Süre sonu değerleri (Nx_n ve Sx_n)
    # Eğer yaş tablosunun sonuna geldiyse hata vermemesi için kontrol ekleyebiliriz
    # ama şimdilik standart varsayıyoruz.
    Nx_n = df.loc[df['yas'] == yas + sure, 'Nx'].values[0]
    Sx_n = df.loc[df['yas'] == yas + sure, 'Sx'].values[0]

    # Formül: Sabit Parça + Değişken Parça
    # Not: degisim_miktari (-) ise matematik otomatik olarak çıkarma yapar.
    
    # (P - d) * a_xn
    sabit_kisim = ((Nx - Nx_n) / Dx) * (baslangic_teminat - degisim_miktari)
    
    # d * (Ia)_xn
    degisken_kisim = ((Sx - Sx_n - (sure * Nx_n)) / Dx) * degisim_miktari
    
    toplam_prim = sabit_kisim + degisken_kisim
    return round(toplam_prim, 4)

# 2. teminat bulma
def adoys_donemsel_teminat(yas, sure, prim, degisim_miktari):
    
    #prim: Müşterinin ödediği Para
    #degisim_miktari: + (Artan) veya - (Azalan)
    
    
    # 1. Komütasyonlar
    Dx = df.loc[df['yas'] == yas, 'Dx'].values[0]
    Nx = df.loc[df['yas'] == yas, 'Nx'].values[0]
    Sx = df.loc[df['yas'] == yas, 'Sx'].values[0]
    
    Nx_n = df.loc[df['yas'] == yas + sure, 'Nx'].values[0]
    Sx_n = df.loc[df['yas'] == yas + sure, 'Sx'].values[0]

    # 2. Katsayılar
    katsayi_sabit = (Nx - Nx_n) / Dx
    katsayi_artan = (Sx - Sx_n - (sure * Nx_n)) / Dx

    # 3. Hesaplama (P'yi bulma)
    pay = prim - (degisim_miktari * katsayi_artan)
    baslangic_teminati = (pay / katsayi_sabit) + degisim_miktari
    
    # --- GÜVENLİK KONTROLÜ (YENİ EKLENDİ) ---
    # Eğer AZALAN bir sigorta ise (-), vade sonunda maaşın eksiye düşüp düşmediğine bak.
    if degisim_miktari < 0:
        son_odeme = baslangic_teminati + ((sure - 1) * degisim_miktari)
        
        if son_odeme < 0:
            return (f"HATA: Yatırılan prim ({prim} TL) bu düşüş miktarını karşılamıyor! "
                    f"Hesaplanan başlangıç maaşı ({round(baslangic_teminati, 2)}) "
                    f"ancak {sure}. yılda maaş eksiye düşüyor ({round(son_odeme, 2)}).")

    return round(baslangic_teminati, 2)



# =============================================================================
# BÖLÜM 3: TEST VE ÇALIŞTIRMA ALANI
# =============================================================================
# Bu kısım sadece dosya doğrudan çalıştırıldığında (Run) devreye girer.
# Başka bir dosyadan 'import' edilirse çalışmaz.

if __name__ == "__main__":
    
    # 1. Adım: Faiz Oranını Belirle ve Tabloyu Hazırla
    TEKNIK_FAIZ = 0.04  # Örn: %4
    komutasyon_hazirla(TEKNIK_FAIZ)
    
    print("=" * 50)
    print(f"HESAPLAMALAR BAŞLATILIYOR (Faiz: %{int(TEKNIK_FAIZ*100)})")
    print("=" * 50)

    if not df.empty:
        # TÖYS Testleri
        print("\n--- TÖYS TESTLERİ ---")
        print(f"Prim Hesabı (21y, 10y, 2000TL):   {toys_prim_hesapla(21, 10, 2000)}")
        print(f"Teminat Hesabı (21y, 10y, 700TL): {toys_teminat_hesapla(21, 10, 700)}")

        # ÖBÖYS Testleri
        print("\n--- ÖBÖYS TESTLERİ ---")
        print(f"Prim (Dönem Başı, 30y, 5000TL):  {oboys_prim_hesaplama1(30, 5000)}")
        print(f"Prim (Dönem Sonu, 30y, 5000TL):  {oboys_prim_hesaplama2(30, 5000)}")
        print(f"Teminat (Dönem Başı, 35y, 1000TL): {oboys_teminat_hesaplama1(35, 1000)}")
        
        # DYS Testleri
        print("\n--- DYS TESTLERİ ---")
        print(f"Prim (Dönem Başı, 25y, 5y, 10k): {dys_prim_hesaplama1(25, 5, 10000)}")
        print(f"Teminat (Dönem Başı, 30y, 10y, 2k): {dys_teminat_hesaplama1(30, 10, 2000)}")

        # EYS Testleri
        print("\n--- EYS TESTLERİ ---")
        print(f"Prim (30y, 5y erteleme, 2000TL): {eys_prim_hesaplama1(30, 5, 2000)}")
        print(f"Teminat (30y, 5y erteleme, 2000TL): {eys_teminat_hesaplama1(30, 5, 2000)}")

        # DVEYS Testleri
        print("\n--- DVEYS TESTLERİ ---")
        print(f"Prim (30y, 5y bekle, 10y al):    {dveys_prim_hesaplama1(30, 5, 10, 2000)}")
        
        # ADOYS Testleri
        print("\n--- ADOYS TESTLERİ (Değişken) ---")
        print(f"Artan Prim (30y, 10k+1k artış):  {adoys_omur_boyu_prim(30, 10000, 1000)}")
        print(f"Artan Teminat (30y, 200k+1k):    {adoys_omurboyu_teminat(30, 200000, 1000)}")
        print(f"Dönemsel Artan Prim (30y, 10y):  {adoys_donemsel_prim(30, 10, 10000, 1000)}")
        print(f"Azalan Prim (30y, 50k - 5k azalış): {adoys_omur_boyu_prim(30, 50000, -5000)}")
        
    else:
        print("HATA: Tablo yüklenemediği için testler çalıştırılamadı.")
    
    print("\n" + "=" * 50)
    print("TEST TAMAMLANDI")
    print("=" * 50)





