#!/bin/bash
# GModStore Job Scraper - Linux Otomatik Kurulum Scripti

set -e

echo "========================================"
echo "GModStore Scraper - Linux Kurulum"
echo "========================================"
echo ""

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Mevcut kullanıcı ve dizin
CURRENT_USER=$(whoami)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo -e "${GREEN}[INFO]${NC} Kullanıcı: $CURRENT_USER"
echo -e "${GREEN}[INFO]${NC} Script Dizini: $SCRIPT_DIR"
echo -e "${GREEN}[INFO]${NC} Proje Dizini: $PROJECT_ROOT"
echo ""

# Python kontrolü
echo -e "${YELLOW}[1/5]${NC} Python kontrol ediliyor..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}[OK]${NC} $PYTHON_VERSION bulundu"
else
    echo -e "${RED}[ERROR]${NC} Python3 bulunamadı!"
    echo "Kurmak için: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

# Virtual environment oluştur
echo ""
echo -e "${YELLOW}[2/5]${NC} Virtual environment oluşturuluyor..."
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    python3 -m venv "$PROJECT_ROOT/venv"
    echo -e "${GREEN}[OK]${NC} venv oluşturuldu"
else
    echo -e "${GREEN}[OK]${NC} venv zaten mevcut"
fi

# Bağımlılıkları yükle
echo ""
echo -e "${YELLOW}[3/5]${NC} Bağımlılıklar yükleniyor..."
source "$PROJECT_ROOT/venv/bin/activate"
pip install -q -r "$PROJECT_ROOT/requirements.txt"
echo -e "${GREEN}[OK]${NC} Bağımlılıklar yüklendi"

# Service dosyasını güncelle
echo ""
echo -e "${YELLOW}[4/5]${NC} Service dosyası hazırlanıyor..."
SERVICE_FILE="$PROJECT_ROOT/deploy/systemd/gmodstore-scraper.service"
SERVICE_FILE_TEMP="$PROJECT_ROOT/gmodstore-scraper.service"

# Service dosyasını geçici olarak kopyala
cp "$SERVICE_FILE" "$SERVICE_FILE_TEMP"

# Kullanıcı ve yolu güncelle
sed -i "s|YOUR_USERNAME|$CURRENT_USER|g" "$SERVICE_FILE_TEMP"
sed -i "s|/home/$CURRENT_USER/gmodstore_scrapper|$PROJECT_ROOT|g" "$SERVICE_FILE_TEMP"

echo -e "${GREEN}[OK]${NC} Service dosyası güncellendi"

# Kurulum talimatları
echo ""
echo -e "${YELLOW}[5/5]${NC} Service kurulumu için aşağıdaki komutları çalıştırın:"
echo ""
echo -e "${GREEN}sudo cp $SERVICE_FILE_TEMP /etc/systemd/system/${NC}"
echo -e "${GREEN}sudo systemctl daemon-reload${NC}"
echo -e "${GREEN}sudo systemctl enable gmodstore-scraper${NC}"
echo -e "${GREEN}sudo systemctl start gmodstore-scraper${NC}"
echo ""

# Config kontrolü
echo "========================================"
if grep -q "BURAYA_WEBHOOK_URL_GIRILECEK" "$PROJECT_ROOT/config.py" 2>/dev/null; then
    echo -e "${RED}[UYARI]${NC} config.py'de DISCORD_WEBHOOK_URL ayarlanmamış!"
    echo "Önce config.py dosyasını düzenleyin:"
    echo "  nano $PROJECT_ROOT/config.py"
else
    echo -e "${GREEN}[OK]${NC} Webhook URL ayarlanmış görünüyor"
fi

echo ""
echo "========================================"
echo -e "${GREEN}Kurulum tamamlandı!${NC}"
echo ""
echo "Manuel test için:"
echo "  cd $PROJECT_ROOT"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Detaylı bilgi: docs/LINUX_KURULUM.md"
echo "========================================"
