# VIX Visualizer Dashboard 📈

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyInstaller](https://img.shields.io/badge/PyInstaller-6.15.0-orange.svg)](https://pyinstaller.org/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

Ett avancerat Python-program som skapar en komplett dashboard för VIX, VVIX och SKEW marknadsriskövervakning med realtidsanalys och trendsignaler.

## ✨ Funktioner

- 📊 **Realtidsdata** för VIX (^VIX), VVIX (^VVIX) och SKEW (^SKEW) via yfinance
- 📈 **Modern dashboard** med översikt, analys och förklaringar
- 🔍 **Avancerad trendanalys** med glidande medelvärden (MA20)
- ⚠️ **Riskvarningar** och marknadsanalys baserat på forskning
- 🌐 **Responsiv design** med Bootstrap och modern CSS
- 📅 **6 månaders data** med automatisk uppdatering
- 🎯 **Risk Score System** med kombinerade varningssignaler
- 📋 **Detaljerad tolkningsguide** för alla index

## 🚀 Snabbstart

### Installation

```bash
# Klona projektet
git clone https://github.com/ditt-användarnamn/vix-visualizer.git
cd vix-visualizer

# Installera beroenden
pip install -r requirements.txt
```

### Kör programmet

```bash
# Kör Python-versionen
python main.py

# Eller kör .exe-versionen (Windows)
./dist/VIXVisualizer.exe
```

### Bygg .exe fil

```bash
# Installera PyInstaller
pip install pyinstaller

# Bygg .exe fil
python -m PyInstaller --onefile --windowed --name "VIXVisualizer" main.py
```

## 📊 Dashboard-funktioner

### 🎯 Risk Score Analysis
- **Formel**: (VIX > 25 → +1) + (VVIX > 120 → +1) + (SKEW > 150 → +1)
- **Varningsnivåer**: Ingen, Lätt, Måttlig, Stark varning
- **Kombinerad analys** av alla tre index

### 📈 Trendanalys
- **Bullish signal**: När volatilitetsindex faller under MA - minskande rädsla
- **Bearish signal**: När volatilitetsindex stiger över MA - ökande oro
- **Neutral**: Blandade signaler - avvakta klarare trendriktning

### 🎨 Modern Design
- **Responsiv layout** med Bootstrap 5
- **Glassmorphism-effekter** med backdrop-filter
- **Hover-animationer** och smooth transitions
- **Färgmatchning** mellan graflinjer och infoboxar

## 📁 Projektstruktur

```
vix-visualizer/
├── main.py                 # Huvudprogrammet
├── requirements.txt        # Python-beroenden
├── test_program.py        # Testscript
├── build_exe.bat         # Windows build-script
├── bypass_smartscreen.bat # SmartScreen bypass
├── INSTALLATION_GUIDE.md  # Användarguide
├── sign_exe_guide.md     # Certifikatsignering
├── CONTRIBUTING.md        # Bidragsguide
├── LICENSE               # MIT-licens
├── .gitignore           # Git ignore-filer
├── dist/                # Byggda .exe filer
│   └── VIXVisualizer.exe
└── README.md            # Denna fil
```

## 🔧 Systemkrav

- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.8+ (för utveckling)
- **RAM**: Minst 4GB
- **Internet**: Krävs för datahämtning
- **Webbläsare**: Chrome, Firefox, Edge

## 📊 Volatilitetsindexen

### VIX (Volatility Index)
- **Risk nivå**: Måttlig Risk
- **Vad det mäter**: Implied volatilitet (30 dagar) på S&P 500
- **Normalt intervall**: 12-20 | **Varningsnivå**: Över 25-30
- **Tolkning**: Förväntad hög volatilitet – ofta vid oro

### VVIX (Volatility of VIX)
- **Risk nivå**: Låg Risk
- **Vad det mäter**: Volatilitet i VIX-indexet
- **Normalt intervall**: 80-100 | **Varningsnivå**: Över 110-120
- **Tolkning**: Osäkerhet i osäkerheten – stressnivå

### SKEW (Tail Risk Index)
- **Risk nivå**: Måttlig Risk
- **Vad det mäter**: Marknadens sannolikhet för extrem nedgång
- **Normalt intervall**: 110-130 | **Varningsnivå**: Över 145-150
- **Tolkning**: Efterfrågan på långt utanför pengarna-putar ökar

## ⚠️ Windows SmartScreen

Om Windows blockerar .exe filen:

1. **Högerklicka** på `VIXVisualizer.exe`
2. Välj **"Kör som administratör"**
3. Klicka **"Ja"** när Windows frågar

Alternativt:
- Klicka **"Mer information"** → **"Kör ändå"**
- Lägg till i **Windows Defender undantag**

## 🤝 Bidra

Se [CONTRIBUTING.md](CONTRIBUTING.md) för detaljerad guide om hur du bidrar till projektet.

### Snabb bidragsprocess:
1. Fork projektet
2. Skapa en feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit dina ändringar (`git commit -m 'Add some AmazingFeature'`)
4. Push till branchen (`git push origin feature/AmazingFeature`)
5. Öppna en Pull Request

## 📄 Licens

Detta projekt är licensierat under MIT-licensen - se [LICENSE](LICENSE) filen för detaljer.

## 🆘 Support

- 📧 **Issues**: [GitHub Issues](https://github.com/ditt-användarnamn/vix-visualizer/issues)
- 📖 **Dokumentation**: [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- 🔧 **Felsökning**: Kör `python test_program.py` för diagnostik

## 🙏 Tack

Tack för att du använder VIX Visualizer! Om du gillar projektet, överväg att:

- ⭐ **Stjärnmärk** projektet på GitHub
- 🐛 **Rapportera buggar** via Issues
- 💡 **Föreslå förbättringar** via Discussions
- 🤝 **Bidra** med kod eller dokumentation

---

**Skapad med ❤️ för avancerad marknadsanalys**

*"Data hämtas från Yahoo Finance via yfinance-biblioteket. Använd på egen risk för investeringsbeslut."* 