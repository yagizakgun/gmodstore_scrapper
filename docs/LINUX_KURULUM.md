# 🐧 Linux'ta Kurulum ve Sürekli Çalıştırma Rehberi

Bu rehber, GModStore Job Scraper botunu Linux sunucunuzda kurup 7/24 çalışır halde tutmanızı sağlar.

## 🌐 Dil / Language

- **[Türkçe](LINUX_KURULUM.md)** (Mevcut)
- **[English](LINUX_INSTALLATION.md)** | **[Ana README](../README.md)**

---

## 📋 Gereksinimler

- Ubuntu 20.04+ / Debian 10+ / CentOS 8+ veya herhangi bir modern Linux dağıtımı
- Python 3.8+
- İnternet erişimi
- sudo yetkisi

---

## 🚀 Hızlı Kurulum

### 1. Dosyaları Sunucuya Yükleyin

Dosyaları sunucunuza kopyalayın (örnek: `/home/kullanici/gmodstore_scrapper`):

```bash
# Git ile clone (önerilen)
cd ~
git clone https://github.com/kullanici_adi/gmodstore_scrapper.git

# Veya SCP ile kopyalama (Windows'tan)
# scp -r gmodstore_scrapper kullanici@sunucu_ip:/home/kullanici/
```

### 2. Python ve Bağımlılıkları Kurun

```bash
# Python ve pip kurulumu (eğer yoksa)
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# Proje dizinine gidin
cd ~/gmodstore_scrapper

# Virtual environment oluşturun
python3 -m venv venv

# Aktif edin
source venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### 3. Konfigürasyonu Ayarlayın

```bash
# config.py dosyasını düzenleyin
nano config.py
```

Discord Webhook URL'nizi ayarlayın ve kaydedin (Ctrl+X, Y, Enter).

### 4. Manuel Test (Opsiyonel)

```bash
# Bot'u test edin
source venv/bin/activate
python main.py
```

Ctrl+C ile durdurun.

---

## 🔄 Systemd ile Otomatik Çalıştırma (Önerilen)

Systemd, botunuzu:
- ✅ Sunucu açıldığında otomatik başlatır
- ✅ Çökerse otomatik yeniden başlatır
- ✅ Log'ları düzenli tutar

### 1. Service Dosyasını Düzenleyin

```bash
# Service dosyasını düzenleyin
nano ~/gmodstore_scrapper/deploy/systemd/gmodstore-scraper.service
```

**Aşağıdaki satırları kendi bilgilerinizle değiştirin:**

```ini
User=YOUR_USERNAME          → User=kullanici_adiniz
Group=YOUR_USERNAME         → Group=kullanici_adiniz
WorkingDirectory=/home/YOUR_USERNAME/gmodstore_scrapper → WorkingDirectory=/home/kullanici_adiniz/gmodstore_scrapper
ExecStart=/home/YOUR_USERNAME/gmodstore_scrapper/venv/bin/python main.py → ExecStart=/home/kullanici_adiniz/gmodstore_scrapper/venv/bin/python main.py
```

### 2. Service'i Sisteme Kurun

```bash
# Service dosyasını kopyalayın
sudo cp ~/gmodstore_scrapper/deploy/systemd/gmodstore-scraper.service /etc/systemd/system/

# Systemd'yi yeniden yükleyin
sudo systemctl daemon-reload

# Service'i etkinleştirin (açılışta başlat)
sudo systemctl enable gmodstore-scraper

# Service'i başlatın
sudo systemctl start gmodstore-scraper
```

### 3. Durumu Kontrol Edin

```bash
# Service durumunu görün
sudo systemctl status gmodstore-scraper
```

Çıktı şöyle görünmeli:

```
● gmodstore-scraper.service - GModStore Job Market Discord Scraper
     Active: active (running) since ...
```

---

## 📊 Yararlı Komutlar

### Service Yönetimi

```bash
# Durumu kontrol et
sudo systemctl status gmodstore-scraper

# Başlat
sudo systemctl start gmodstore-scraper

# Durdur
sudo systemctl stop gmodstore-scraper

# Yeniden başlat
sudo systemctl restart gmodstore-scraper

# Açılışta başlamayı kapat
sudo systemctl disable gmodstore-scraper
```

### Log'ları Görüntüleme

```bash
# Son log'ları görüntüle
sudo journalctl -u gmodstore-scraper -n 50

# Canlı log takibi
sudo journalctl -u gmodstore-scraper -f

# Bugünün log'ları
sudo journalctl -u gmodstore-scraper --since today

# Son 1 saatin log'ları
sudo journalctl -u gmodstore-scraper --since "1 hour ago"
```

---

## 🔧 Sorun Giderme

### "Permission denied" Hatası

```bash
# Dosya izinlerini düzeltin
chmod +x ~/gmodstore_scrapper/main.py
chmod 755 ~/gmodstore_scrapper
```

### Service Başlamıyor

```bash
# Detaylı hata mesajını görün
sudo journalctl -u gmodstore-scraper -n 100 --no-pager

# Manuel çalıştırarak test edin
cd ~/gmodstore_scrapper
source venv/bin/activate
python main.py
```

### Python Bulunamıyor

```bash
# Python yolunu kontrol edin
which python3

# Service dosyasında ExecStart'ı tam yol ile güncelleyin
# Örnek: ExecStart=/usr/bin/python3 main.py
```

### Webhook Hatası

```bash
# config.py'yi kontrol edin
cat ~/gmodstore_scrapper/config.py | grep WEBHOOK

# URL'nin doğru olduğundan emin olun
```

---

## 🔄 Güncelleme Yapma

```bash
# Service'i durdurun
sudo systemctl stop gmodstore-scraper

# Güncellemeleri yapın (dosyaları değiştirin veya git pull)
cd ~/gmodstore_scrapper
# ... değişiklikler ...

# Bağımlılıkları güncelleyin (gerekirse)
source venv/bin/activate
pip install -r requirements.txt

# Service'i yeniden başlatın
sudo systemctl start gmodstore-scraper
```

---

## 🐳 Alternatif: Docker ile Çalıştırma (Opsiyonel)

Docker kullanmak isterseniz:

```bash
# Docker kurulumu
sudo apt install docker.io -y
sudo systemctl enable docker
sudo systemctl start docker

# Dockerfile oluşturun (zaten projede var)
cd ~/gmodstore_scrapper
docker build -t gmodstore-scraper -f deploy/docker/Dockerfile .

# Çalıştırın
docker run -d --name gmodstore-scraper --restart=always gmodstore-scraper
```

---

## 📝 Notlar

1. **Güvenlik**: `config.py` dosyanızdaki webhook URL'si hassas bilgidir. Dosya izinlerini kısıtlayın:
   ```bash
   chmod 600 ~/gmodstore_scrapper/config.py
   ```

2. **Performans**: Bot çok az kaynak kullanır (~20-50MB RAM).

3. **Zaman Dilimi**: Sunucunuzun zaman dilimini ayarlayın:
   ```bash
   sudo timedatectl set-timezone Europe/Istanbul
   ```

4. **Firewall**: Giden HTTPS bağlantılarına (443) izin verin (genelde varsayılan olarak açık).

---

## ❓ Sık Sorulan Sorular

**S: Bot ne kadar RAM kullanır?**
C: Yaklaşık 20-50MB RAM.

**S: Sunucu kapanırsa ne olur?**
C: Systemd sayesinde sunucu açıldığında bot otomatik başlar.

**S: Bot çökerse?**
C: Systemd 10 saniye sonra otomatik yeniden başlatır.

**S: Log'lar disk dolduruyor mu?**
C: Hayır, journald otomatik log rotasyonu yapar.

---

**İyi kullanımlar! 🚀**

---

**[View English Version](LINUX_INSTALLATION.md)** | **[View Main README](../README.md)**
