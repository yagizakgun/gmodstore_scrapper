# GModStore Job Market Discord Scraper

GModStore'daki iş ilanlarını otomatik olarak takip eden ve yeni ilanları Discord kanalınıza gönderen Python uygulaması.

## 🌐 Dil / Language

- **[Türkçe](README_TR.md)** (Mevcut)
- **[English](../README.md)**

---

## Özellikler

- ✅ 30 dakikada bir otomatik kontrol
- ✅ Sadece aktif ilanları gönderir (Apply, In Progress, Negotiations)
- ✅ **YENİ**: Her ilanın detay sayfasından bilgi çeker (Bütçe, Kategori, Başvurular, Görüntüleme)
- ✅ **YENİ**: Otomatik son başvuru tarihi kontrolü - süresi geçmiş ilanları filtreler
- ✅ **YENİ**: İlk başlatmada eski/süresi geçmiş ilanları göndermez
- ✅ Kapsamlı bilgilerle güzel Discord embed mesajları
- ✅ Tekrarlayan mesaj önleme sistemi
- ✅ Graceful shutdown (Ctrl+C ile güvenli kapanma)
- ✅ Rate limit koruması

## Kurulum

### 1. Gereksinimler

- Python 3.8 veya üzeri
- Windows PowerShell (Windows için) veya Terminal (Linux/Mac için)

### 2. Proje Kurulumu

**Windows:**

```powershell
# Proje dizinine git
cd gmodstore_scrapper

# Virtual environment oluştur
python -m venv venv

# Virtual environment'ı aktifleştir
.\venv\Scripts\Activate.ps1

# Bağımlılıkları kur
pip install -r requirements.txt
```

**Linux/Mac:**

```bash
# Proje dizinine git
cd gmodstore_scrapper

# Virtual environment oluştur
python3 -m venv venv

# Virtual environment'ı aktifleştir
source venv/bin/activate

# Bağımlılıkları kur
pip install -r requirements.txt
```

### 3. Discord Webhook Oluşturma

1. Discord sunucunuzda, iş ilanlarını almak istediğiniz kanala gidin
2. Kanal ayarlarına tıklayın (⚙️)
3. **Entegrasyonlar** → **Webhook'lar** → **Yeni Webhook**
4. Webhook'a bir isim verin (örn: "GModStore Jobs")
5. **Webhook URL'sini Kopyala** butonuna tıklayın

### 4. Yapılandırma

`config.py` dosyasını açın ve Discord webhook URL'nizi yapıştırın:

```python
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."
```

## Kullanım

### Başlatma

```powershell
# Virtual environment aktifken
python main.py
```

### Arka Planda Çalıştırma

**Windows:**

```powershell
# PowerShell'de arka planda başlatma
Start-Process -NoNewWindow python -ArgumentList "main.py"
```

**Linux/Mac:**

```bash
# Arka planda başlatma
nohup python main.py &
```

### Durdurma

- **Ctrl+C** tuşlarına basın (graceful shutdown)
- Veya konsol penceresini kapatın

## Discord Embed Formatı

Her yeni ilan şu formatta gönderilir:

```
┌─────────────────────────────────────────────┐
│ [GModStore Logo]                            │
│                                             │
│ Looking for a Helix Gmod developer...       │
│ (Başlık - tıklanabilir link)                │
│                                             │
│ 💰 Budget: $100.00                          │
│ 📁 Category: Gamemode                       │
│ 📊 Status: 🟢 Apply                         │
│ 📝 Applications: 2                          │
│ 👁️ Views: 47                                │
│ ⏰ Due Date: 2026-02-01                     │
│                                             │
│ Description:                                │
│ [Açıklama metni]                            │
│                                             │
│ Footer: GModStore Job Market                │
└─────────────────────────────────────────────┘
```

**Not:** Bu format Discord embed mesajı olarak gönderilir ve görsel olarak düzenlenmiş bir şekilde görünür.

### Durum Renkleri

- 🟢 **Apply** → Yeşil
- 🟡 **In Progress** → Sarı
- 🟠 **Negotiations** → Turuncu
- ⚫ **Finished** → Gri (gönderilmez)

## Dosya Yapısı

```
gmodstore_scrapper/
├── main.py              # Ana uygulama
├── scraper.py           # GModStore scraper
├── discord_webhook.py   # Discord mesaj gönderimi
├── config.py            # Yapılandırma
├── requirements.txt     # Python bağımlılıkları
├── seen_jobs.json       # Görülen ilanlar (otomatik oluşur)
├── venv/                # Virtual environment (gitignore'da)
├── README.md            # Ana README (İngilizce)
└── docs/                # Dokümantasyon klasörü
    ├── README_TR.md         # Türkçe versiyon
    ├── INSTALLATION.md      # Windows kurulum rehberi (İngilizce)
    ├── KURULUM.md           # Windows kurulum rehberi (Türkçe)
    ├── LINUX_INSTALLATION.md # Linux kurulum rehberi (İngilizce)
    └── LINUX_KURULUM.md     # Linux kurulum rehberi (Türkçe)
```

## Yapılandırma Seçenekleri

`config.py` dosyasında şunları değiştirebilirsiniz:

| Ayar | Varsayılan | Açıklama |
|------|-----------|----------|
| `CHECK_INTERVAL` | 1800 (30dk) | Kontrol aralığı (saniye) |
| `DETAIL_REQUEST_DELAY` | 1.5 | Detay sayfası istekleri arası gecikme (saniye) |
| `ACTIVE_JOB_STATUSES` | Apply, In Progress, Negotiations | Gönderilecek durum tipleri |
| `STATUS_COLORS` | ... | Discord embed renkleri |

## Sorun Giderme

### "Webhook test başarısız" hatası

- Discord webhook URL'sinin doğru olduğundan emin olun
- Webhook'un silinmediğinden emin olun
- İnternet bağlantınızı kontrol edin

### "Hiç ilan bulunamadı" uyarısı

- GModStore'un erişilebilir olduğunu kontrol edin
- HTML yapısı değişmiş olabilir (scraper.py güncellenmeli)
- `scraper.py`'yi test modunda çalıştırın: `python scraper.py`

### Tüm ilanlar süresi geçmiş olarak filtrelendi

- GModStore'daki tüm ilanların son başvuru tarihi geçmişse bu normaldir
- Sistem spam önlemek için süresi geçmiş ilanları otomatik filtreler
- Yeni aktif ilanlar göründüğünde otomatik olarak gönderilecektir

### Virtual environment aktif değil

**Windows:**

```powershell
.\venv\Scripts\Activate.ps1
```

Eğer hata alırsanız, PowerShell execution policy'sini değiştirin:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

## Test Modları

### Scraper Testi

```powershell
python scraper.py
```

### Discord Webhook Testi

```powershell
python discord_webhook.py
```

## Güncellemeler

```powershell
# Virtual environment aktifken
pip install --upgrade -r requirements.txt
```

## Dokümantasyon

- **[Windows Kurulum Rehberi (İngilizce)](INSTALLATION.md)**
- **[Windows Kurulum Rehberi (Türkçe)](KURULUM.md)**
- **[Linux Kurulum Rehberi (İngilizce)](LINUX_INSTALLATION.md)**
- **[Linux Kurulum Rehberi (Türkçe)](LINUX_KURULUM.md)**
- **[Değişiklik Günlüğü](../CHANGELOG.md)** - Versiyon geçmişi ve güncellemeler

## Lisans

MIT License

## İletişim

Sorularınız için GitHub Issues kullanabilirsiniz.

---

**Not:** Bu scraper GModStore'un robot.txt kurallarına uyar ve makul rate limiting kullanır. Lütfen sorumlu kullanın.
