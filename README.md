# 📊 Hayat_Sigortalari

## 👤 Geliştirici Hakkında

**İsim Soyisim:** *Sude Sert*

**Üniversite:** *Selçuk Üniversitesi*

**Bölüm:** *Aktüerya Bilimleri / 3. sınıf*

**İletişim:** *sudesert81@gmail.com veya www.linkedin.com/in/sudesert*

---
## 📝 Proje Hakkında

Bu proje, aktüeryal hesaplamaların dijitalleştirilmesi amacıyla tasarlanmış üç aşamalı bir projenin ilk adımıdır (Modül 1-Yasam Sigortaları). Akademik çalışmalarım kapsamında TRSH-2010 (Türkiye Sigortalı Hayat Tablosu) Mortalite Tablosu verilerini Python programlama dili ile entegre ederek paranın zaman değerini modellemektedir.

- TRSH-2010 Erkek sigortalı hayat tablosu verileri işlenmektedir.
- Kullanıcı tarafından belirlenen teknik faiz oranına göre dinamik olarak komütasyon sütunları (Dx, Nx, Sx, Cx, Mx, Rx ) hesaplanmaktadır. 
- Yaşam sigortalarında prim ve teminat hesabını kapsar
- Modül-1, hayat sigortaları kapsamındaki yaşam olasılıklarını baz alarak prim ve teminat hesaplama süreçlerini dijitalleştirmektedir.

---
## ⚠️ Kapsam ve Teknik Detaylar
Bu modül sadece **"Yaşam Teminatlı" (Survival Benefits)** ürünleri kapsamaktadır.
* **Dahil Olanlar:** Saf Kapital, Ömür Boyu Rantlar, Süreli Rantlar (Kişi yaşadığı sürece ödeme yapılanlar).
* **Veri Seti:** TRSH-2010 Erkek sigortalı hayat tablosu.
* **Komütasyon:** Kullanıcı tarafından belirlenen teknik faiz oranına göre dinamik olarak hesaplanan $D_x, N_x, S_x$ sütunları.

---
## 🛠️ Kurulum ve Çalıştırma Aşamaları

Bu modülü yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyiniz.

1. Gereksinimler
Sisteminizde Python 3.x kurulu olmalıdır. Ayrıca gerekli kütüphaneyi yüklemek için terminale/komut satırına şu kodu yazın:
pip install pandas

2. Dosya Hazırlığı
Proje dosyalarını (Modul1_Yasam_Sigortalari.py, README.md ve TRSH2010_Erkek.csv) aynı klasöre indirin.

    *Önemli: Python kodundaki dosya_yolu değişkenini, TRSH2010_Erkek.csv dosyasının bilgisayarınızdaki konumuyla güncelleyin.*

3. Çalıştırma
Spyder, VS Code veya herhangi bir Python IDE'sini açın.
**Modul1_Yasam_Sigortalari.py** dosyasını çalıştırın.
Konsol ekranında hesaplama özetini ve net tek prim sonucunu göreceksiniz.

>NOT: Tablo dosyasında ayırıcı olarak ‘;’ ve ondalık işareti olarak ‘,’ kullanılmaktadır. Kod bu formatı otomatik olarak işleyecek şekilde yapılandırılmıştır.

---
## 💻 Kullanım Örneği 

Kodları çalıştırmadan önce tablonun yüklendiğinden ve faiz oranının belirlendiğinden emin olun.

### 1. Hazırlık Aşaması
İlk olarak kütüphaneyi çağırıp teknik faiz oranını (Örn: %3) belirliyoruz.

```python
# %3 Faiz oranı ile komütasyon sayılarını hazırla
komutasyon_hazirla(0.03)

#Tek Ödemeli Yaşam Sigortası (toys)
# Parametreler: (yas, sure, hedef_para)
prim = toys_prim_hesapla(25, 10, 50000)

print(f"Ödenmesi Gereken Peşin Prim: {prim} TL")

#Ömür Boyu Ödemeli Yaşam Sigortası (oboys)
# Parametreler: (yas, istenen_maas)
maliyet = oboys_prim_hesaplama1(30, 5000)

print(f"Ömür Boyu Maaşın Maliyeti: {maliyet} TL")

#Dönemsel Yaşam Sigortası (dys)
# Parametreler: (yas, sure, eldeki_para)
maas = dys_teminat_hesaplama1(40, 15, 100000)

print(f"100.000 TL ile alınabilecek yıllık maaş: {maas} TL")

#Aritmetik Değişken Ödemeli Yaşam Sigortası (adoys) 
# Parametreler: (yas, baslangic_maasi, artis_miktari)
# Artış miktarı (+) girilirse Artan, (-) girilirse Azalan hesaplar.
degisken_prim = adoys_omur_boyu_prim(30, 10000, 1000)

print(f"Artan Maaş Sigortası Primi: {degisken_prim} TL")
```

---
## 📚 Fonksiyon Rehberi

Bu kütüphanedeki fonksiyonlar genel olarak iki sonek (suffix) ile biter:
* `_prim_hesapla`: Belirli bir maaşı almak için bugün yatırılması gereken parayı (Maliyeti) bulur.
* `_teminat_hesapla`: Belirli bir toplu para ile ne kadar maaş bağlanabileceğini (Faydayı) bulur.

### 1. TÖYS (Tek Ödemeli Yaşam Sigortası)
Saf Kapital (Pure Endowment) olarak da bilinir.
* **Fonksiyon:** `toys_...`
* **Ne Yapar?**: Kişi belirlenen süre sonunda (n yıl) hâlâ hayattaysa tek seferlik toplu ödeme yapar. Arada ölürse ödeme yapılmaz.

### 2. ÖBÖYS (Ömür Boyu Ödemeli Yaşam Sigortası)
* **Fonksiyon:** `oboys_...`
* **Ne Yapar?**: Kişi yaşadığı sürece sonsuza dek (ölene kadar) düzenli maaş öder.
    * `hesaplama1`: Dönem Başı (Ödemeler hemen başlar).
    * `hesaplama2`: Dönem Sonu (Ödemeler 1 yıl sonra başlar).

### 3. DYS (Dönemsel Yaşam Sigortası)
Süreli Rant (Temporary Annuity) olarak bilinir.
* **Fonksiyon:** `dys_...`
* **Ne Yapar?**: Sadece belirli bir süre (örneğin 10 yıl) boyunca maaş öder. Süre bitince kişi yaşasa bile ödeme kesilir.

### 4. EYS (Ertelenmiş Yaşam Sigortası)
Deferred Annuity olarak bilinir.
* **Fonksiyon:** `eys_...`
* **Ne Yapar?**: Ödemeler hemen başlamaz, belirlenen bir bekleme süresinden (r yıl) sonra başlar.

### 5. DVEYS (Dönemsel ve Ertelenmiş Yaşam Sigortası)
* **Fonksiyon:** `dveys_...`
* **Ne Yapar?**: Hem ertelenmiş (beklemeli) hem de süreli (kısıtlı) olan sigorta türüdür. Örneğin: "5 yıl bekle, sonra 10 yıl maaş al".

### 6. ADOYS (Aritmetik Değişken Yaşam Sigortası) 🔥
En gelişmiş modüldür.
* **Fonksiyon:** `adoys_...`
* **Ne Yapar?**: Sabit değil, her yıl belirli bir tutarda artan (+) veya azalan (-) maaşları hesaplar.
* **Özellik:** Azalan sigortalarda maaşın eksiye düşüp düşmediğini otomatik kontrol eder (Smart Safety Check).




