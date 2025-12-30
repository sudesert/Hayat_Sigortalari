# Hayat_Sigortalari

## Geliştirici Hakkında

**İsim Soyisim:** *Sude Sert*

**Üniversite:** *Selçuk Üniversitesi*

**Bölüm:** *Aktüerya Bilimleri / 3. sınıf*

**İletişim:** *sudesert81@gmail.com veya www.linkedin.com/in/sudesert*

---
## Proje Hakkında

Bu proje, aktüeryal hesaplamaların dijitalleştirilmesi amacıyla tasarlanmış üç aşamalı bir projenin ilk adımıdır (Modül-1). Akademik çalışmalarım kapsamında TRSH-2010 (Türkiye Sigortalı Hayat Tablosu) Mortalite Tablosu verilerini Python programlama dili ile entegre ederek paranın zaman değerini modellemektedir.

- TRSH-2010 Erkek sigortalı hayat tablosu verileri işlenmektedir.
- Kullanıcı tarafından belirlenen teknik faiz oranına göre dinamik olarak komütasyon sütunları (Dx, Nx, Sx, Cx, Mx, Rx ) hesaplanmaktadır. 
- Yaşam sigortalarında prim ve teminat hesabını kapsar
- Modül-1, hayat sigortaları kapsamındaki yaşam olasılıklarını baz alarak prim ve teminat hesaplama süreçlerini dijitalleştirmektedir.
---
## Kurulum ve Çalıştırma Aşamaları

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
