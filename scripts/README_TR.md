# Scripts

Bu klasör uygulamayı başlatmak ve kurmak için kullanılan script dosyalarını içerir.

## Dosyalar

- **start.bat** - Windows için başlatma scripti
- **setup_linux.sh** - Linux için otomatik kurulum scripti

## Kullanım

### Windows

`start.bat` dosyasına çift tıklayarak uygulamayı başlatabilirsiniz. Script otomatik olarak:
1. Proje root dizinine geçer
2. Virtual environment'ı aktifleştirir
3. Uygulamayı başlatır

### Linux

Kurulum scriptini çalıştırın:

```bash
chmod +x scripts/setup_linux.sh
./scripts/setup_linux.sh
```

Script otomatik olarak:
1. Python kontrolü yapar
2. Virtual environment oluşturur
3. Bağımlılıkları yükler
4. Systemd service dosyasını hazırlar
5. Kurulum talimatlarını gösterir

Detaylı bilgi için:
- [Windows Kurulum Rehberi](../docs/KURULUM.md)
- [Linux Kurulum Rehberi](../docs/LINUX_KURULUM.md)

---

**[View English Version](README.md)**
