OHHamLogger - Radioamatöörilokiohjelma
Suomeksi
OHHamLogger - Versio 1.2.0
OHHamLogger on yksinkertainen ja tehokas lokinpito-ohjelma radioamatööreille. Ohjelma tukee ADI 3.1.0 -formaatia ja WWFF-lokien tallennusta.
Uudet Ominaisuudet Versiossa 1.2.0
1. Automaattinen Varmuuskopiointi
Minuutin välin varmuuskopiot: Ohjelma luo automaattisesti varmuuskopion nykyisestä lokista minuutin välein
Älykäs tiedostonhallinta: Varmuuskopiot nimetään aikaleimalla: backup_YYYYMMDD_HHMMSS_alkuperainennimi.adi
Automaattinen siivous: Säilyttää vain 10 uusinta varmuuskopiota, vanhat poistetaan automaattisesti
Konfiguroitavissa: Varmuuskopiointi voidaan ottaa pois päältä asetuksista
2. Tekstitiedostolokin Tuonti
Monipuolinen tuontituki: Tuo QSO-tietueita useista yleisistä tekstimuodoista:
OH2ABC 59 59 2024-01-15 14:30 20m SSB
2024-01-15 14:30 OH2ABC 20m SSB 59 59
CSV-muoto: OH2ABC,59,59,2024-01-15,14:30,20m,SSB
Älykäs jäsennys: Automaattisesti tunnistaa päivämäärän, ajan, kutsun, bandin, moden ja RST-raportit
Duplikaattitarkistus: Estää saman QSO:n tuomisen useita kertoja
3. Paranneltu Englannin Kielen Tuki
Kattava lokalisaatio: Kaikki uudet toiminnot käännetty englanniksi
Yhdenmukainen käyttöliittymä: Kaikki valikot, painikkeet ja viestit saatavilla molemmilla kielillä
Helppo kielen vaihto: Asetuksista voi vaihtaa kielen suomen ja englannin välillä
Perusominaisuudet
QSO-lokinpito: Nopea ja helppo syöttö syöttörivin kautta
ADI 3.1.0 -tuki: Tuo ja vie standardimuotoisia ADI-tiedostoja
WWFF-lokitus: Automaattinen WWFF-tietueiden käsittely
Pikavalinnat: Nopeat bandi- ja mode-valinnat painikkeilla
Tilastot: Reaaliaikaiset tilastot QSO-määristä
Teemat: Useita visuaalisia teemoja (oletus, suomi, yömodi, meri, joulu, retro, jne.)
Lokkien yhdistäminen: Yhdistä useita ADI-lokkeja yhdeksi tiedostoksi
Osittainen vienti: Vie vain tietyn ajanjakson QSO:t
Asennus ja Käyttö
1. Asennus:
bash
python OHHamLog1.2.0.py
2. Ensimmäinen käyttö:
Aseta oma kutsu, locator ja WWFF-alue asetuksista
Aloita uusi loki tai jatka edellistä
3. QSO:n syöttö:
Kirjoita syöttöriville: "OH2ABC 59 59 kommentti"
Vaihda bandia/modea pikakomennoilla (numerot/kirjaimet)
4. Tallennus:
Tallenna ADI-muodossa: Tiedosto ? Tallena ADI
Tekninen Tieto
Kehitetty: Python 3 & Tkinter
Ylläpitäjä: OH3ENK
Lisenssi: Open Source
Lähdekoodi: Saatavilla SourceForgessa

OHHamLogger - Radio Amateur Logging Software
In English
OHHamLogger - Version 1.2.0
OHHamLogger is a simple and efficient logging software for radio amateurs. The program supports ADI 3.1.0 format and WWFF logging.
New Features in Version 1.2.0
1. Automatic Backup
Minute-interval backups: Program automatically creates backups of current log every minute
Smart file management: Backups are timestamped: backup_YYYYMMDD_HHMMSS_originalname.adi
Automatic cleanup: Keeps only 10 most recent backups, old ones are automatically removed
Configurable: Backup can be disabled in settings
2. Text File Log Import
Versatile import support: Import QSO records from multiple common text formats:
OH2ABC 59 59 2024-01-15 14:30 20m SSB
2024-01-15 14:30 OH2ABC 20m SSB 59 59
CSV format: OH2ABC,59,59,2024-01-15,14:30,20m,SSB
Smart parsing: Automatically recognizes date, time, callsign, band, mode and RST reports
Duplicate checking: Prevents importing the same QSO multiple times
3. Enhanced English Language Support
Comprehensive localization: All new features translated to English
Consistent interface: All menus, buttons and messages available in both languages
Easy language switching: Change language between Finnish and English in settings
Core Features
QSO logging: Fast and easy input through input line
ADI 3.1.0 support: Import and export standard ADI files
WWFF logging: Automatic WWFF record handling
Quick controls: Fast band and mode selection with buttons
Statistics: Real-time statistics of QSO counts
Themes: Multiple visual themes (default, finnish, night mode, sea, christmas, retro, etc.)
Log merging: Combine multiple ADI logs into one file
Partial export: Export only QSOs from specific time period
Installation and Usage
1. Installation:
bash
python OHHamLog1.2.0.py
2. First use:
Set your callsign, locator and WWFF area in settings
Start new log or continue previous one
3. Entering QSO:
Type in input line: "OH2ABC 59 59 comment"
Change band/mode with quick commands (numbers/letters)
4. Saving:
Save in ADI format: File ? Save ADI
Technical Information
Developed in: Python 3 & Tkinter
Maintainer: OH3ENK
License: Open Source
Source code: Available on SourceForge

Kehittäjä/Developer: OH3ENK
Yhteystiedot/Contact: OH3ENK@oh3enk.fi
Lähdekoodi/Source Code: http://sourceforge.net/projects/ohhamlogger


