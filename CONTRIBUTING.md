# 🤝 Bidra till VIX Visualizer

Tack för ditt intresse för att bidra till VIX Visualizer! Detta dokument innehåller riktlinjer för att bidra till projektet.

## 🚀 Snabbstart

### Förutsättningar
- Python 3.8+
- Git
- Internetanslutning

### Installation
```bash
# Klona projektet
git clone https://github.com/ditt-användarnamn/vix-visualizer.git
cd vix-visualizer

# Skapa virtuell miljö
python -m venv venv
source venv/bin/activate  # Linux/Mac
# eller
venv\Scripts\activate     # Windows

# Installera beroenden
pip install -r requirements.txt
```

## 📝 Bidragsprocess

### 1. Skapa en Issue
- Beskriv problemet eller förslaget tydligt
- Inkludera steg för att reproducera (om bugg)
- Ange din miljö (OS, Python-version)

### 2. Fork och Clone
```bash
# Fork projektet på GitHub
# Klona din fork
git clone https://github.com/ditt-användarnamn/vix-visualizer.git
```

### 3. Skapa en Branch
```bash
git checkout -b feature/din-funktion
# eller
git checkout -b fix/ditt-problem
```

### 4. Gör ändringar
- Följ kodstilen (se nedan)
- Lägg till tester om möjligt
- Uppdatera dokumentation

### 5. Testa
```bash
# Kör programmet
python main.py

# Testa att bygga .exe
python -m PyInstaller --onefile --windowed main.py
```

### 6. Commit och Push
```bash
git add .
git commit -m "Lägg till: beskrivning av ändringen"
git push origin feature/din-funktion
```

### 7. Skapa Pull Request
- Beskriv ändringarna tydligt
- Länka till relevant issue
- Vänta på review

## 📋 Kodstil

### Python
- Använd **PEP 8** standard
- Max 120 tecken per rad
- Använd f-strings för formatering
- Lägg till docstrings för funktioner

### HTML/CSS
- Använd 2 mellanslag för indentation
- Använd semantisk HTML
- Följ BEM-metodik för CSS-klasser

### JavaScript
- Använd ES6+ syntax
- Använd `const` och `let` istället för `var`
- Använd arrow functions när möjligt

## 🧪 Testning

### Manuell testning
```bash
# Testa datahämtning
python test_program.py

# Testa huvudprogrammet
python main.py
```

### Automatiserad testning (framtida)
```bash
# Kör tester
python -m pytest tests/

# Kör med coverage
python -m pytest --cov=main tests/
```

## 📚 Dokumentation

### Uppdatera README
- Beskriv nya funktioner
- Uppdatera skärmdumpar
- Lägg till användningsexempel

### Uppdatera Installation Guide
- Beskriv nya krav
- Uppdatera felsökningssteg
- Lägg till nya systemkrav

## 🏷️ Commit Messages

Använd konventionella commit-meddelanden:

```
feat: lägg till ny funktion
fix: åtgärda bugg
docs: uppdatera dokumentation
style: formatering
refactor: omstrukturera kod
test: lägg till tester
chore: underhåll
```

## 🔍 Review Process

### Som bidragsgivare
- Besvara kommentarer snabbt
- Gör nödvändiga ändringar
- Testa efter ändringar

### Som reviewer
- Var konstruktiv
- Fokusera på kod, inte person
- Förklara varför ändringar behövs

## 🎯 Prioriterade områden

### Hög prioritet
- [ ] Förbättra felhantering
- [ ] Lägg till fler test
- [ ] Optimera prestanda
- [ ] Förbättra användargränssnitt

### Medel prioritet
- [ ] Lägg till fler volatilitetsindex
- [ ] Implementera caching
- [ ] Förbättra mobil responsivitet
- [ ] Lägg till export-funktioner

### Låg prioritet
- [ ] Lägg till dark mode
- [ ] Implementera notifikationer
- [ ] Lägg till fler språk
- [ ] Skapa API

## 📞 Support

Om du har frågor:
- Skapa en issue på GitHub
- Beskriv problemet tydligt
- Inkludera felmeddelanden

## 🙏 Tack

Tack för att du bidrar till VIX Visualizer! Ditt bidrag hjälper till att göra projektet bättre för alla användare. 