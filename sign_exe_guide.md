# 🔐 Signera VIXVisualizer.exe med Certifikat

## Problem
Windows SmartScreen blockerar `.exe` filer som inte är signerade med ett betrott certifikat.

## Lösningar

### 1. Enkel lösning - Kör ändå
```
1. Högerklicka på VIXVisualizer.exe
2. Välj "Egenskaper"
3. Klicka "Avblockera" (om tillgängligt)
4. Klicka "Kör som administratör"
```

### 2. Skapa självsignerat certifikat (för utvecklare)

#### Steg 1: Installera OpenSSL
```bash
# Ladda ner från: https://slproweb.com/products/Win32OpenSSL.html
# Eller använd Chocolatey:
choco install openssl
```

#### Steg 2: Skapa certifikat
```bash
# Skapa privat nyckel
openssl genrsa -out private.key 2048

# Skapa certifikat
openssl req -new -x509 -key private.key -out certificate.crt -days 365

# Konvertera till PFX
openssl pkcs12 -export -out certificate.pfx -inkey private.key -in certificate.crt
```

#### Steg 3: Signera .exe
```bash
# Installera signtool (del av Windows SDK)
# Eller använd osslsigncode:
osslsigncode -sign certificate.pfx -in VIXVisualizer.exe -out VIXVisualizer_signed.exe
```

### 3. Professionell lösning - Köp certifikat
- **DigiCert** - $99/år
- **Sectigo** - $99/år  
- **GlobalSign** - $199/år

## Rekommendation
För personligt bruk: Använd "Kör ändå"
För kommersiell distribution: Köp ett betrott certifikat 