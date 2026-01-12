# Hızlı Kurulum Rehberi

## 🌐 Dil / Language

- **[Türkçe](KURULUM.md)** (Mevcut)
- **[English](INSTALLATION.md)** | **[Ana README](../README.md)**

---

## 1. Discord Webhook URL Alma

1. Discord sunucunuzda bir kanal seçin (örn: #gmodstore-jobs)
2. Kanal ayarlarına gidin (⚙️ simgesi)
3. **Entegrasyonlar** → **Webhook'lar**
4. **Yeni Webhook** butonuna tıklayın
5. Webhook'a bir isim verin: "GModStore Jobs"
6. **Webhook URL'sini Kopyala** butonuna tıklayın

## 2. Webhook URL'yi Yapılandırma

`config.py` dosyasını bir metin editörü ile açın ve şu satırı bulun:

```python
DISCORD_WEBHOOK_URL = "BURAYA_WEBHOOK_URL_GIRILECEK"
```

Tırnak işaretleri arasına kopyaladığınız webhook URL'sini yapıştırın:

```python
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz"
```

Dosyayı kaydedin ve kapatın.

## 3. Uygulamayı Başlatma

### Yöntem 1: Batch Dosyası ile (Önerilen)

`scripts/start.bat` dosyasına çift tıklayın. Uygulama otomatik olarak başlayacaktır.

### Yöntem 2: PowerShell ile

```powershell
# Proje klasörüne gidin
cd gmodstore_scrapper

# Virtual environment'ı aktifleştirin
.\venv\Scripts\Activate.ps1

# Uygulamayı başlatın
python main.py
```

## 4. Uygulamanın Çalışıp Çalışmadığını Kontrol Etme

Uygulama başarıyla başladığında:

1. Discord kanalınızda "🚀 GModStore Job Scraper Başlatıldı" mesajını göreceksiniz
2. Konsol çıktısında şu mesajları göreceksiniz:

```powershell
================================================
GModStore Job Market Discord Scraper
================================================
[SUCCESS] Webhook test başarılı!
[INFO] Bot başlatıldı. Ctrl+C ile durdurun.
```

## 5. Çalışma Mantığı

- Uygulama **30 dakikada bir** GModStore'u kontrol eder
- Yeni iş ilanlarını bulduğunda Discord'a gönderir
- Aynı ilanı birden fazla kez göndermez (seen_jobs.json ile takip eder)
- Sadece **aktif ilanları** gönderir (Apply, In Progress, Negotiations)
- "Finished" durumundaki ilanlar gönderilmez

## 6. Uygulamayı Durdurma

- **Ctrl+C** tuşlarına basın
- Veya konsol penceresini kapatın

Uygulama kapatılırken görülen ilanların listesini kaydeder, böylece tekrar başlattığınızda aynı ilanları tekrar göndermez.

## 7. Ayarları Değiştirme

`config.py` dosyasında şunları değiştirebilirsiniz:

### Kontrol Aralığını Değiştirme

```python
CHECK_INTERVAL = 1800  # 30 dakika (saniye cinsinden)
```

Örnek değerler:
- 5 dakika: `300`
- 15 dakika: `900`
- 30 dakika: `1800`
- 1 saat: `3600`

### Gönderilecek İlan Durumlarını Değiştirme

```python
ACTIVE_JOB_STATUSES = ["Apply", "In Progress", "Negotiations"]
```

Sadece yeni ilanları göndermek için:
```python
ACTIVE_JOB_STATUSES = ["Apply"]
```

### Discord Embed Renklerini Değiştirme

```python
STATUS_COLORS = {
    "Apply": 0x00FF00,        # Yeşil
    "In Progress": 0xFFFF00,  # Sarı
    "Negotiations": 0xFFA500, # Turuncu
    "Finished": 0x808080      # Gri
}
```

Renk kodları hex formatında (0x ile başlayan 6 haneli kod).

## 8. Sorun Giderme

### "PowerShell execution policy" hatası

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "DISCORD_WEBHOOK_URL ayarlanmamış" hatası

`config.py` dosyasında webhook URL'sini doğru ayarladığınızdan emin olun.

### "Webhook test başarısız" hatası

- Webhook URL'sinin doğru olduğunu kontrol edin
- İnternet bağlantınızı kontrol edin
- Webhook'un Discord'da silinmediğini kontrol edin

### Hiç ilan gelmiyorsa

1. GModStore'da yeni ilan olup olmadığını manuel olarak kontrol edin
2. `scraper.py` dosyasını test modunda çalıştırın:
   ```powershell
   python scraper.py
   ```
3. HTML yapısı değişmiş olabilir, bu durumda scraper güncellemesi gerekir

## 9. Otomatik Başlatma (Windows Başlangıcı)

Windows'un başlangıcında otomatik çalışması için:

1. `Win + R` tuşlarına basın
2. `shell:startup` yazıp Enter'a basın
3. `start.bat` dosyasının kısayolunu bu klasöre kopyalayın

Ya da Task Scheduler kullanarak daha gelişmiş ayarlar yapabilirsiniz.

## Destek

Herhangi bir sorun yaşarsanız, `main.py` çalışırken konsol çıktısını kontrol edin. 
Hata mesajları `[ERROR]` etiketi ile başlar.

---

**[View English Version](INSTALLATION.md)** | **[View Main README](../README.md)**
