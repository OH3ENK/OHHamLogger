#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import os
import json
import re
from pathlib import Path

class HamLogger:
    def __init__(self, root):
        self.root = root
        self.root.title("OHHamLogger")
        self.root.geometry("1000x700")
        
        # Kieli-asetus
        self.language = 'suomi'
        self.version = "1.0.0"
        
        # Nykyinen lokitiedosto
        self.current_log_file = None
        self.log_modified = False
        
        # Oletusasetukset
        self.settings = {
            'mycall': 'OH3ENK',
            'mylocator': 'KP20TH',
            'mywwff': 'OHFF-0029',
            'default_band': '20m',
            'default_mode': 'SSB',
            'default_rst_sent': '59',
            'default_rst_rcvd': '59',
            'data_dir': os.path.join(os.path.expanduser('~'), 'hamlog', 'adi'),
            'theme': 'oletus',
            'language': 'suomi'
        }
        
        # Nykyiset asetukset
        self.current_band = self.settings['default_band']
        self.current_mode = self.settings['default_mode']
        self.log_entries = []
        
        self.load_settings()
        self.setup_data_dir()
        self.update_language()
        self.create_widgets()
        self.start_clock()
        self.apply_theme()
        
    def setup_data_dir(self):
        """Luo tietokansiot tarvittaessa"""
        Path(self.settings['data_dir']).mkdir(parents=True, exist_ok=True)
    
    def load_settings(self):
        """Lataa asetukset tiedostosta"""
        try:
            settings_file = os.path.join(os.path.expanduser('~'), 'hamlog', 'settings.json')
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # Päivitä vain olemassa olevat avaimet
                    for key in self.settings:
                        if key in loaded_settings:
                            self.settings[key] = loaded_settings[key]
                    
                    self.language = self.settings.get('language', 'suomi')
        except Exception as e:
            print(f"Asetustiedoston lataus epäonnistui: {e}")
    
    def save_settings(self):
        """Tallenna asetukset tiedostoon"""
        try:
            settings_file = os.path.join(os.path.expanduser('~'), 'hamlog', 'settings.json')
            Path(settings_file).parent.mkdir(parents=True, exist_ok=True)
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Asetustiedoston tallennus epäonnistui: {e}")
    
    def update_language(self):
        """Päivitä käyttöliittymän kieli"""
        if self.language == 'english':
            self.texts = {
                'file_menu': "File",
                'new_log': "New Log",
                'open_log': "Open Log", 
                'save_log': "Save Log",
                'save_log_as': "Save Log As",
                'export_partial': "Export Partial Log",
                'exit': "Exit",
                'settings_menu': "Settings",
                'station_info': "Station Information",
                'info_menu': "Information",
                'about': "About",
                'help_menu': "Help",
                'help': "Help",
                'qso_log': "QSO Log",
                'input': "Input",
                'input_line': "Input line:",
                'quick_controls': "Quick Controls",
                'bands': "Bands:",
                'modes': "Modes:",
                'time': "Time",
                'current_settings': "Current Settings",
                'previous_contact': "Previous Contact",
                'stats': "Statistics",
                'total_qsos': "Total QSOs:",
                'today': "Today:",
                'switch_log': "Switch Log",
                'save_adi': "Save ADI",
                'open_log_btn': "Open Log",
                'save_exit': "Save and Exit",
                'first_contact': "FIRST CONTACT",
                'previous_with_station': "PREVIOUSLY WITH STATION:",
                'save_changes': "Save changes?",
                'save_changes_question': "Do you want to save changes to current log before",
                'no_open_log': "No open log",
                'log': "Log:",
                'modified': " *",
                'no_contacts': "No contacts",
                'no_data': "No data",
                'no_qso_data': "No QSO data found in file",
                'file_open_error': "File open error",
                'file_save_error': "File save error",
                'export_complete': "Export complete",
                'about_title': "About HamLogger",
                'about_text': f"HamLogger - Radio Amateur Logging Software\nVersion {self.version}\nDeveloped by OH3ENK\n\nSimple and efficient logging for radio amateurs\nSupports ADI 3.1.0 format and WWFF logging"
            }
        else:  # suomi
            self.texts = {
                'file_menu': "Tiedosto",
                'new_log': "Uusi loki",
                'open_log': "Avaa loki",
                'save_log': "Tallenna loki", 
                'save_log_as': "Tallenna loki nimellä",
                'export_partial': "Vie osa lokista",
                'exit': "Poistu",
                'settings_menu': "Asetukset",
                'station_info': "Radioaseman tiedot",
                'info_menu': "Tietoa",
                'about': "Tietoa ohjelmasta",
                'help_menu': "Ohje",
                'help': "Ohje",
                'qso_log': "QSO Loki",
                'input': "Syöttö",
                'input_line': "Syöttörivi:",
                'quick_controls': "Pikavalinnat",
                'bands': "Bandit:",
                'modes': "Modet:",
                'time': "Aika",
                'current_settings': "Nykyiset Asetukset",
                'previous_contact': "Edellinen yhteys",
                'stats': "Tilastot",
                'total_qsos': "QSOt yhteensä:",
                'today': "Tänään:",
                'switch_log': "Vaihda lokia",
                'save_adi': "Tallenna ADI",
                'open_log_btn': "Avaa loki",
                'save_exit': "Tallenna ja sulje",
                'first_contact': "ENSIMMÄINEN YHTEYS",
                'previous_with_station': "AIEMMIN SAMAN ASEMAN KANSSA:",
                'save_changes': "Tallenna muutokset?",
                'save_changes_question': "Haluatko tallentaa muutokset nykyiseen lokiin ennen",
                'no_open_log': "Ei avointa lokia",
                'log': "Loki:",
                'modified': " *",
                'no_contacts': "Ei yhteyksiä",
                'no_data': "Ei dataa",
                'no_qso_data': "Tiedostosta ei löytynyt luettavaa QSO-dataa",
                'file_open_error': "Avausvirhe",
                'file_save_error': "Tallennusvirhe",
                'export_complete': "Vienti valmis",
                'about_title': "Tietoa HamLoggerista",
                'about_text': f"HamLogger - Radioamatöörilokiohjelma\nVersio {self.version}\nKehittänyt OH3ENK\n\nYksinkertainen ja tehokas lokinpito radioamatööreille\nTuki ADI 3.1.0 -formaattiin ja WWFF-lokeihin"
            }
        
        # Päivitä käyttöliittymän tekstit
        self.update_ui_texts()
    
    def update_ui_texts(self):
        """Päivitä kaikki käyttöliittymän tekstit dynaamisesti"""
        if hasattr(self, 'file_label'):
            file_info = self.texts['no_open_log']
            if self.current_log_file:
                filename = os.path.basename(self.current_log_file)
                file_info = f"{self.texts['log']} {filename}"
                if self.log_modified:
                    file_info += self.texts['modified']
            self.file_label.config(text=file_info)
        
        # Päivitä muut käyttöliittymän osat
        if hasattr(self, 'log_frame'):
            self.log_frame.config(text=self.texts['qso_log'])
        
        if hasattr(self, 'input_frame'):
            self.input_frame.config(text=self.texts['input'])
            self.input_frame.winfo_children()[0].config(text=self.texts['input_line'])
        
        if hasattr(self, 'controls_frame'):
            self.controls_frame.config(text=self.texts['quick_controls'])
        
        if hasattr(self, 'clock_frame'):
            self.clock_frame.config(text=self.texts['time'])
        
        if hasattr(self, 'settings_frame'):
            self.settings_frame.config(text=self.texts['current_settings'])
        
        if hasattr(self, 'prev_contact_frame'):
            self.prev_contact_frame.config(text=self.texts['previous_contact'])
        
        if hasattr(self, 'stats_frame'):
            self.stats_frame.config(text=self.texts['stats'])
        
        # Päivitä painikkeet
        if hasattr(self, 'switch_log_btn'):
            self.switch_log_btn.config(text=self.texts['switch_log'])
        
        if hasattr(self, 'save_adi_btn'):
            self.save_adi_btn.config(text=self.texts['save_adi'])
        
        if hasattr(self, 'open_log_btn'):
            self.open_log_btn.config(text=self.texts['open_log_btn'])
        
        if hasattr(self, 'save_exit_btn'):
            self.save_exit_btn.config(text=self.texts['save_exit'])
        
        # Päivitä tilastot
        if hasattr(self, 'total_qso_label'):
            total = len(self.log_entries)
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            today_count = sum(1 for qso in self.log_entries if qso['timestamp'].startswith(today))
            self.total_qso_label.config(text=f"{self.texts['total_qsos']} {total}")
            self.today_qso_label.config(text=f"{self.texts['today']} {today_count}")
    
    def apply_theme(self):
        """Sovelleta valittu teema"""
        theme = self.settings.get('theme', 'oletus')
        
        if theme == 'syksyinen metsä':
            self.root.configure(bg='#2E8B57')
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('TFrame', background='#2E8B57')
            style.configure('TLabel', background='#2E8B57', foreground='#FFFFFF')
            style.configure('TButton', background='#D2691E', foreground='#FFFFFF')
            style.configure('TLabelframe', background='#2E8B57', foreground='#FFFFFF')
            style.configure('TLabelframe.Label', background='#2E8B57', foreground='#FFFFFF')
            style.configure('TEntry', fieldbackground='#FFFFFF')
        
        elif theme == 'suomi':
            self.root.configure(bg='#FFFFFF')
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('TFrame', background='#FFFFFF')
            style.configure('TLabel', background='#FFFFFF', foreground='#003580')
            style.configure('TButton', background='#003580', foreground='#FFFFFF')
            style.configure('TLabelframe', background='#FFFFFF', foreground='#003580')
            style.configure('TLabelframe.Label', background='#FFFFFF', foreground='#003580')
            style.configure('TEntry', fieldbackground='#FFFFFF')
        
        elif theme == 'yömodi':
            self.root.configure(bg='#2C2C2C')
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('TFrame', background='#2C2C2C')
            style.configure('TLabel', background='#2C2C2C', foreground='#E0E0E0')
            style.configure('TButton', background='#404040', foreground='#FFFFFF')
            style.configure('TLabelframe', background='#2C2C2C', foreground='#E0E0E0')
            style.configure('TLabelframe.Label', background='#2C2C2C', foreground='#E0E0E0')
            style.configure('TEntry', fieldbackground='#404040', foreground='#FFFFFF')
        
        elif theme == 'meri':
            self.root.configure(bg='#87CEEB')
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('TFrame', background='#87CEEB')
            style.configure('TLabel', background='#87CEEB', foreground='#000080')
            style.configure('TButton', background='#4682B4', foreground='#FFFFFF')
            style.configure('TLabelframe', background='#87CEEB', foreground='#000080')
            style.configure('TLabelframe.Label', background='#87CEEB', foreground='#000080')
            style.configure('TEntry', fieldbackground='#FFFFFF')
        
        elif theme == 'kulta':
            self.root.configure(bg='#DAA520')
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('TFrame', background='#DAA520')
            style.configure('TLabel', background='#DAA520', foreground='#8B4513')
            style.configure('TButton', background='#CD853F', foreground='#FFFFFF')
            style.configure('TLabelframe', background='#DAA520', foreground='#8B4513')
            style.configure('TLabelframe.Label', background='#DAA520', foreground='#8B4513')
            style.configure('TEntry', fieldbackground='#FFFFFF')
        
        elif theme == 'joulu':
            self.root.configure(bg='#8B0000')
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('TFrame', background='#8B0000')
            style.configure('TLabel', background='#8B0000', foreground='#FFFFFF')
            style.configure('TButton', background='#228B22', foreground='#FFFFFF')
            style.configure('TLabelframe', background='#8B0000', foreground='#FFFFFF')
            style.configure('TLabelframe.Label', background='#8B0000', foreground='#FFFFFF')
            style.configure('TEntry', fieldbackground='#FFFFFF')
        
        elif theme == 'retro':
            self.root.configure(bg='#FF69B4')
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('TFrame', background='#FF69B4')
            style.configure('TLabel', background='#FF69B4', foreground='#000000')
            style.configure('TButton', background='#00FFFF', foreground='#000000')
            style.configure('TLabelframe', background='#FF69B4', foreground='#000000')
            style.configure('TLabelframe.Label', background='#FF69B4', foreground='#000000')
            style.configure('TEntry', fieldbackground='#FFFFFF')
        
        elif theme == 'elegantti':
            self.root.configure(bg='#F8F8F8')
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('TFrame', background='#F8F8F8')
            style.configure('TLabel', background='#F8F8F8', foreground='#333333')
            style.configure('TButton', background='#333333', foreground='#FFFFFF')
            style.configure('TLabelframe', background='#F8F8F8', foreground='#333333')
            style.configure('TLabelframe.Label', background='#F8F8F8', foreground='#333333')
            style.configure('TEntry', fieldbackground='#FFFFFF')
        
        else:
            self.root.configure(bg='#F0F0F0')
            style = ttk.Style()
            style.theme_use('clam')
    
    def create_widgets(self):
        # Päävalikko
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Tiedosto-valikko
        self.file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.texts['file_menu'], menu=self.file_menu)
        self.file_menu.add_command(label=self.texts['new_log'], command=self.new_log)
        self.file_menu.add_command(label=self.texts['open_log'], command=self.open_log_file)
        self.file_menu.add_command(label=self.texts['save_log'], command=self.save_current_log)
        self.file_menu.add_command(label=self.texts['save_log_as'], command=self.save_log_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=self.texts['export_partial'], command=self.export_partial_log)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=self.texts['exit'], command=self.quit_application)
        
        # Asetukset-valikko
        self.settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.texts['settings_menu'], menu=self.settings_menu)
        self.settings_menu.add_command(label=self.texts['station_info'], command=self.edit_settings)
        
        # Tietoa-valikko
        self.info_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.texts['info_menu'], menu=self.info_menu)
        self.info_menu.add_command(label=self.texts['about'], command=self.show_about)
        
        # Ohje-valikko
        self.help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.texts['help_menu'], menu=self.help_menu)
        self.help_menu.add_command(label=self.texts['help'], command=self.show_help)
        
        # Päänäkymä
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ylätason info-paneeli
        self.create_header(main_frame)
        
        # Pääsisältö frame
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Vasen paneeli (loki ja syöttö)
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Log-näkymä
        self.create_log_view(left_frame)
        
        # Syöttöruutu
        self.create_input_section(left_frame)
        
        # Nopeat valintapainikkeet
        self.create_quick_controls(left_frame)
        
        # Painikkeet
        self.create_buttons(left_frame)
        
        # Oikea paneeli (info)
        right_frame = ttk.Frame(content_frame, width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)
        
        # Info-paneeli
        self.create_info_section(right_frame)
        
        self.input_entry.focus()
    
    def create_header(self, parent):
        """Luo ylätason header"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Nykyinen lokitiedosto
        file_info = self.texts['no_open_log']
        if self.current_log_file:
            filename = os.path.basename(self.current_log_file)
            file_info = f"{self.texts['log']} {filename}"
            if self.log_modified:
                file_info += self.texts['modified']
        
        self.file_label = ttk.Label(header_frame, text=file_info, font=('Helvetica', 10, 'bold'))
        self.file_label.pack(side=tk.LEFT)
        
        # Vaihda loki -painike
        self.switch_log_btn = ttk.Button(header_frame, text=self.texts['switch_log'], command=self.switch_log)
        self.switch_log_btn.pack(side=tk.RIGHT)
    
    def create_log_view(self, parent):
        """Luo lokinäkymän"""
        self.log_frame = ttk.LabelFrame(parent, text=self.texts['qso_log'], padding="5")
        self.log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Luo Text widget tagit erilaisille tyyleille
        self.log_text = tk.Text(self.log_frame, height=20, width=70, font=('Courier New', 9))
        
        # Määritä tyylit
        self.log_text.tag_configure("duplicate", foreground="red", font=('Courier New', 9, 'bold'))
        self.log_text.tag_configure("normal", foreground="black")
        
        scrollbar = ttk.Scrollbar(self.log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_input_section(self, parent):
        """Luo syöttöosion"""
        self.input_frame = ttk.LabelFrame(parent, text=self.texts['input'], padding="5")
        self.input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.input_frame, text=self.texts['input_line']).grid(row=0, column=0, sticky=tk.W)
        self.input_entry = ttk.Entry(self.input_frame, width=60)
        self.input_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        self.input_entry.bind('<Return>', self.process_input)
        self.input_entry.bind('<KeyRelease>', self.check_special_input)
        
        self.input_frame.columnconfigure(1, weight=1)
    
    def create_quick_controls(self, parent):
        """Luo nopeat band/mode valitsimet"""
        self.controls_frame = ttk.LabelFrame(parent, text=self.texts['quick_controls'], padding="5")
        self.controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Band-painikkeet
        band_frame = ttk.Frame(self.controls_frame)
        band_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(band_frame, text=self.texts['bands']).pack(side=tk.LEFT)
        
        common_bands = ['160m', '80m', '60m', '40m', '30m', '20m', '17m', '15m', '12m', '10m', '6m', '2m', '70cm']
        for band in common_bands:
            btn = ttk.Button(band_frame, text=band, 
                           command=lambda b=band: self.quick_band_change(b),
                           width=5)
            btn.pack(side=tk.LEFT, padx=1)
        
        # Mode-painikkeet
        mode_frame = ttk.Frame(self.controls_frame)
        mode_frame.pack(fill=tk.X)
        
        ttk.Label(mode_frame, text=self.texts['modes']).pack(side=tk.LEFT)
        
        common_modes = ['SSB', 'LSB', 'USB', 'CW', 'FM', 'AM', 'FT8', 'FT4', 'RTTY']
        for mode in common_modes:
            btn = ttk.Button(mode_frame, text=mode,
                           command=lambda m=mode: self.quick_mode_change(m),
                           width=5)
            btn.pack(side=tk.LEFT, padx=1)
    
    def create_buttons(self, parent):
        """Luo toimintopainikkeet"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X)
        
        self.save_adi_btn = ttk.Button(button_frame, text=self.texts['save_adi'], command=self.save_adi_dialog)
        self.save_adi_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.open_log_btn = ttk.Button(button_frame, text=self.texts['open_log_btn'], command=self.open_log_file)
        self.open_log_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_exit_btn = ttk.Button(button_frame, text=self.texts['save_exit'], command=self.save_and_exit)
        self.save_exit_btn.pack(side=tk.LEFT)
    
    def create_info_section(self, parent):
        """Luo info-osion oikealle puolelle"""
        # UTC-kello
        self.clock_frame = ttk.LabelFrame(parent, text=self.texts['time'], padding="10")
        self.clock_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.clock_label = ttk.Label(self.clock_frame, text="UTC: --:--:--", font=('Courier', 14, 'bold'))
        self.clock_label.pack()
        
        # Nykyiset asetukset
        self.settings_frame = ttk.LabelFrame(parent, text=self.texts['current_settings'], padding="10")
        self.settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.current_band_label = ttk.Label(self.settings_frame, text=f"Band: {self.current_band}", font=('Helvetica', 11))
        self.current_band_label.pack(anchor=tk.W, pady=2)
        
        self.current_mode_label = ttk.Label(self.settings_frame, text=f"Mode: {self.current_mode}", font=('Helvetica', 11))
        self.current_mode_label.pack(anchor=tk.W, pady=2)
        
        # Edellinen yhteys
        self.prev_contact_frame = ttk.LabelFrame(parent, text=self.texts['previous_contact'], padding="10")
        self.prev_contact_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.prev_contact_label = ttk.Label(self.prev_contact_frame, text=self.texts['no_contacts'], wraplength=250)
        self.prev_contact_label.pack(anchor=tk.W)
        
        # Tilastot
        self.stats_frame = ttk.LabelFrame(parent, text=self.texts['stats'], padding="10")
        self.stats_frame.pack(fill=tk.X)
        
        self.total_qso_label = ttk.Label(self.stats_frame, text=f"{self.texts['total_qsos']} 0")
        self.total_qso_label.pack(anchor=tk.W, pady=2)
        
        self.today_qso_label = ttk.Label(self.stats_frame, text=f"{self.texts['today']} 0")
        self.today_qso_label.pack(anchor=tk.W, pady=2)
    
    def show_about(self):
        """Näytä tietoa ohjelmasta -dialogi"""
        messagebox.showinfo(self.texts['about_title'], self.texts['about_text'])
    
    def show_help(self):
        """Näytä ohje"""
        help_text = """
HAMLOGGER - KÄYTTÖOHJE

Peruskäyttö:
1. Aseta asetukset: Asetukset → Radioaseman tiedot
2. Aloita uusi loki: Tiedosto → Uusi loki
3. Syötä QSO: kirjoita syöttöriville "OH2ABC 59 59 kommentti"
4. Tallenna: Tiedosto → Tallena ADI

Pikakomennot:
- Numerot (20, 40, 80): Vaihda bandia
- Kirjaimet (SSB, CW, FM): Vaihda modeta
- Pilkku + numero (,70): Vaihda cm-bandiin

WWFF-lokitus:
- Ohjelma tukee automaattisesti WWFF-lokien tallennusta
- Tiedostonimi muodostuu automaattisesti: OMAKUTSU@WWFF-ALUE.adi

Lisätietoja: https://github.com/oh3enk/hamlogger
        """
        if self.language == 'english':
            help_text = """
HAMLOGGER - USER GUIDE

Basic Usage:
1. Set settings: Settings → Station Information
2. Start new log: File → New Log
3. Enter QSO: type "OH2ABC 59 59 comment" in input line
4. Save: File → Save ADI

Quick Commands:
- Numbers (20, 40, 80): Change band
- Letters (SSB, CW, FM): Change mode
- Comma + number (,70): Change to cm band

WWFF Logging:
- Program automatically supports WWFF logging
- Filename generated automatically: MYCALL@WWFF-AREA.adi

More info: https://github.com/oh3enk/hamlogger
            """
        
        # Luo uusi ikkuna ohjeelle
        help_window = tk.Toplevel(self.root)
        help_window.title(self.texts['help'])
        help_window.geometry("600x400")
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.insert(1.0, help_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(help_window, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def start_clock(self):
        """Käynnistä UTC-kello"""
        self.update_clock()
    
    def update_clock(self):
        """Päivitä UTC-kello sekunneilla"""
        utc_time = datetime.datetime.utcnow().strftime('UTC: %H:%M:%S')
        self.clock_label.config(text=utc_time)
        self.root.after(1000, self.update_clock)
    
    def quick_band_change(self, band):
        """Nopea bandin vaihto"""
        self.current_band = band
        self.update_info_display()
        self.input_entry.focus()
    
    def quick_mode_change(self, mode):
        """Nopea moden vaihto"""
        self.current_mode = mode
        self.update_info_display()
        self.input_entry.focus()
    
    def update_info_display(self):
        """Päivitä info-näkymät"""
        self.current_band_label.config(text=f"Band: {self.current_band}")
        self.current_mode_label.config(text=f"Mode: {self.current_mode}")
    
    def check_special_input(self, event=None):
        """Tarkista erikoissyötteet reaaliajassa"""
        text = self.input_entry.get().strip().upper()
        
        if not text:
            return
        
        # Pilkun jälkeinen luku tulkitaan cm-bandiksi
        if ',' in text:
            parts = text.split(',')
            if len(parts) == 2 and parts[1].strip().isdigit():
                cm_value = parts[1].strip()
                if 1 <= len(cm_value) <= 3:
                    self.current_band = f"{cm_value}cm"
                    self.update_info_display()
                    return
        
        # Pelkkä numerosarja (1-4 numeroa) - vaihda band
        if text.isdigit() and 1 <= len(text) <= 4:
            self.current_band = f"{text}m"
            self.update_info_display()
        
        # Pelkkä kirjainsarja (1-4 kirjainta) - vaihda mode
        elif text.isalpha() and 1 <= len(text) <= 4:
            mode_map = {
                'SSB': 'SSB', 'LSB': 'LSB', 'USB': 'USB', 'CW': 'CW', 
                'FM': 'FM', 'AM': 'AM', 'FT8': 'FT8', 'FT4': 'FT4',
                'RTTY': 'RTTY', 'PSK': 'PSK', 'JT65': 'JT65'
            }
            if text in mode_map:
                self.current_mode = mode_map[text]
                self.update_info_display()
    
    def process_input(self, event=None):
        """Käsittele syöttörivin tiedot"""
        text = self.input_entry.get().strip().upper()
        if not text:
            return
        
        # Tarkista ensin erikoiskomennot (band/mode vaihto)
        if len(text.split()) == 1:
            # Pilkun jälkeinen luku cm-bandiksi
            if ',' in text:
                parts = text.split(',')
                if len(parts) == 2 and parts[1].strip().isdigit():
                    cm_value = parts[1].strip()
                    if 1 <= len(cm_value) <= 3:
                        self.current_band = f"{cm_value}cm"
                        self.update_info_display()
                        self.input_entry.delete(0, tk.END)
                        return "break"
            
            # Numerosarja bandiksi
            if text.isdigit() and 1 <= len(text) <= 4:
                self.current_band = f"{text}m"
                self.update_info_display()
                self.input_entry.delete(0, tk.END)
                return "break"
            
            # Kirjainsarja modeksi
            elif text.isalpha() and 1 <= len(text) <= 4:
                mode_map = {
                    'SSB': 'SSB', 'LSB': 'LSB', 'USB': 'USB', 'CW': 'CW', 
                    'FM': 'FM', 'AM': 'AM', 'FT8': 'FT8', 'FT4': 'FT4',
                    'RTTY': 'RTTY', 'PSK': 'PSK', 'JT65': 'JT65'
                }
                if text in mode_map:
                    self.current_mode = mode_map[text]
                    self.update_info_display()
                    self.input_entry.delete(0, tk.END)
                    return "break"
        
        # Käsitellään QSO-tietue
        if len(text.split()) >= 2:
            parts = text.split()
            callsign = parts[0]
            rst_sent = self.settings['default_rst_sent']
            rst_rcvd = self.settings['default_rst_rcvd']
            comment = ""
            their_wwff = ""  # Vasta-aseman WWFF-tunnus
            
            # Etsi RST:t ja WWFF-tunnus
            if len(parts) >= 3:
                if parts[1].isdigit() and parts[2].isdigit():
                    rst_sent = parts[1]
                    rst_rcvd = parts[2]
                    
                    # Etsi WWFF-tunnus (FF-alkuinen) RST:den jälkeen
                    remaining_parts = parts[3:]
                    for i, part in enumerate(remaining_parts):
                        # Tarkista onko osa WWFF-tunnus (FF-alkuinen)
                        if part.startswith('FF-') or (len(part) >= 5 and part[:2] == 'FF' and part[2] in '0123456789'):
                            their_wwff = part
                            # Poista WWFF-tunnus kommentista
                            remaining_parts.pop(i)
                            break
                        # Tarkista onko osa WWFF-tunnus muodossa OHEF-1234 tms
                        elif '-' in part and len(part.split('-')) == 2:
                            prefix, number = part.split('-')
                            if (len(prefix) == 4 and prefix[:2] in ['FF', 'OH', 'DL', 'SM', 'LA', 'OE', 'PA', 'G', 'GM', 'GW', 'GI', 'GM', 'GU'] and 
                                number.isdigit() and 1 <= len(number) <= 4):
                                their_wwff = part
                                remaining_parts.pop(i)
                                break
                    
                    comment = " ".join(remaining_parts) if remaining_parts else ""
                else:
                    # Ei RST:itä, etsi WWFF-tunnus suoraan
                    for i, part in enumerate(parts[1:]):
                        if part.startswith('FF-') or (len(part) >= 5 and part[:2] == 'FF' and part[2] in '0123456789'):
                            their_wwff = part
                            # Poista WWFF-tunnus kommentista
                            remaining_parts = parts[1:i] + parts[i+1:]
                            comment = " ".join(remaining_parts) if remaining_parts else ""
                            break
                        elif '-' in part and len(part.split('-')) == 2:
                            prefix, number = part.split('-')
                            if (len(prefix) == 4 and prefix[:2] in ['FF', 'OH', 'DL', 'SM', 'LA', 'OE', 'PA', 'G', 'GM', 'GW', 'GI', 'GM', 'GU'] and 
                                number.isdigit() and 1 <= len(number) <= 4):
                                their_wwff = part
                                remaining_parts = parts[1:i] + parts[i+1:]
                                comment = " ".join(remaining_parts) if remaining_parts else ""
                                break
                    else:
                        comment = " ".join(parts[1:]) if len(parts) > 1 else ""
            else:
                comment = " ".join(parts[1:]) if len(parts) > 1 else ""
            
            # CW-mode erikoiskäsittely
            if self.current_mode == 'CW':
                if len(rst_sent) == 2:
                    rst_sent += '9'
                if len(rst_rcvd) == 2:
                    rst_rcvd += '9'
            
            # Luo QSO-tietue
            qso_data = {
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'call': callsign,
                'band': self.current_band,
                'mode': self.current_mode,
                'rst_sent': rst_sent,
                'rst_rcvd': rst_rcvd,
                'comment': comment,
                'my_gridsquare': self.settings['mylocator'],
                'their_wwff': their_wwff  # Tallennetaan vasta-aseman WWFF-tunnus
            }
            
            self.log_entries.append(qso_data)
            self.add_to_log_display(qso_data)
            self.update_stats()
            self.update_previous_contact(qso_data)
            self.log_modified = True
            self.update_header()
        
        self.input_entry.delete(0, tk.END)
        return "break"
    
    def is_duplicate_contact(self, qso_data):
        """Tarkista onko yhteys duplikaatti (sama kutsu, sama päivä, sama bandi, sama mode)"""
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        base_call = qso_data['call'].split('/')[0]
        
        for qso in self.log_entries:
            if qso == qso_data:
                continue
                
            qso_base_call = qso['call'].split('/')[0]
            qso_date = qso['timestamp'].split(' ')[0]
            
            # Tarkista sama kutsu, sama päivä, sama bandi JA sama mode
            if (qso_base_call == base_call and 
                qso_date == today and 
                qso['band'] == qso_data['band'] and 
                qso['mode'] == qso_data['mode']):
                return True
        return False
    
    def add_to_log_display(self, qso_data):
        """Lisää QSO lokinäkymään"""
        log_line = f"{qso_data['timestamp']} | {self.settings['mycall']} > {qso_data['call']} | RST: {qso_data['rst_sent']}/{qso_data['rst_rcvd']} | Band: {qso_data['band']} | Mode: {qso_data['mode']}"
        
        # Näytä WWFF-tunnus lokissa jos se on olemassa
        if qso_data.get('their_wwff'):
            log_line += f" | WWFF: {qso_data['their_wwff']}"
        
        if qso_data['comment']:
            log_line += f" | Comment: {qso_data['comment']}"
        
        log_line += "\n"
        
        # Käytä parannettua duplikaattitarkistusta
        if self.is_duplicate_contact(qso_data):
            self.log_text.insert(tk.END, log_line, "duplicate")
        else:
            self.log_text.insert(tk.END, log_line, "normal")
        
        self.log_text.see(tk.END)
    
    def update_previous_contact(self, qso_data):
        """Päivitä edellinen yhteys saman aseman kanssa -info"""
        base_call = qso_data['call'].split('/')[0]
        same_station_qsos = []
        
        for qso in self.log_entries:
            if qso['call'].split('/')[0] == base_call and qso != qso_data:
                same_station_qsos.append(qso)
        
        if same_station_qsos:
            prev_qso = same_station_qsos[-1]
            
            prev_date = datetime.datetime.strptime(prev_qso['timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y')
            info_text = f"{self.texts['previous_with_station']}\n"
            info_text += f"{prev_date} - {prev_qso['timestamp'].split(' ')[1][:5]}\n"
            info_text += f"Band: {prev_qso['band']} | Mode: {prev_qso['mode']}\n"
            info_text += f"RST: {prev_qso['rst_sent']}/{prev_qso['rst_rcvd']}"
            
            if prev_qso['comment']:
                info_text += f"\nComment: {prev_qso['comment']}"
        else:
            info_text = f"{self.texts['first_contact']}\n{base_call}\nBand: {qso_data['band']}\nMode: {qso_data['mode']}"
        
        self.prev_contact_label.config(text=info_text)
    
    def update_stats(self):
        """Päivitä tilastot"""
        total = len(self.log_entries)
        
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        today_count = sum(1 for qso in self.log_entries if qso['timestamp'].startswith(today))
        
        self.total_qso_label.config(text=f"{self.texts['total_qsos']} {total}")
        self.today_qso_label.config(text=f"{self.texts['today']} {today_count}")
    
    def update_header(self):
        """Päivitä header-tiedot"""
        file_info = self.texts['no_open_log']
        if self.current_log_file:
            filename = os.path.basename(self.current_log_file)
            file_info = f"{self.texts['log']} {filename}"
            if self.log_modified:
                file_info += self.texts['modified']
        
        self.file_label.config(text=file_info)
    
    def switch_log(self):
        """Vaihda lokia"""
        if self.log_modified:
            response = messagebox.askyesnocancel(
                self.texts['save_changes'], 
                f"{self.texts['save_changes_question']} vaihtoa?"
            )
            if response is None:
                return
            elif response:
                self.save_current_log()
        
        self.open_log_file()
    
    def new_log(self):
        """Luo uusi loki"""
        if self.log_modified:
            response = messagebox.askyesnocancel(
                self.texts['save_changes'],
                f"{self.texts['save_changes_question']} uuden luomista?"
            )
            if response is None:
                return
            elif response:
                self.save_current_log()
        
        self.log_entries = []
        self.current_log_file = None
        self.log_modified = False
        self.log_text.delete(1.0, tk.END)
        self.update_stats()
        self.prev_contact_label.config(text=self.texts['no_contacts'])
        self.update_header()
    
    def open_log_file(self):
        """Avaa lokitiedosto"""
        filename = filedialog.askopenfilename(
            initialdir=self.settings['data_dir'],
            filetypes=[("ADI-tiedostot", "*.adi"), ("Text files", "*.txt"), ("Kaikki tiedostot", "*.*")],
            title="Valitse lokitiedosto"
        )
        
        if filename:
            try:
                content = None
                encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                
                for encoding in encodings:
                    try:
                        with open(filename, 'r', encoding=encoding) as f:
                            content = f.read()
                        print(f"Tiedosto luettu onnistuneesti enkoodauksella: {encoding}")
                        break
                    except UnicodeDecodeError:
                        continue
                
                if content is None:
                    messagebox.showerror(self.texts['file_open_error'], "Tiedoston enkoodausta ei tunnistettu. Kokeile muuntaa tiedosto UTF-8 -muotoon.")
                    return
                
                success_count = self.parse_adi_content(content)
                
                if success_count > 0:
                    self.current_log_file = filename
                    self.log_modified = False
                    self.update_header()
                    messagebox.showinfo("Avattu", f"Loki ladattu! {success_count} QSO:ta tuotu.")
                    
                    self.update_stats()
                    self.log_text.delete(1.0, tk.END)
                    for qso in self.log_entries:
                        self.add_to_log_display(qso)
                    
                    if self.log_entries:
                        self.update_previous_contact(self.log_entries[-1])
                else:
                    messagebox.showwarning(self.texts['no_data'], self.texts['no_qso_data'])
                
            except Exception as e:
                messagebox.showerror(self.texts['file_open_error'], f"Tiedoston avaus epäonnistui: {str(e)}")
    
    def parse_adi_content(self, content):
        """Jäsennä ADI-muotoinen sisältö"""
        success_count = 0
        self.log_entries = []
        
        header_end = content.find('<EOH>')
        if header_end != -1:
            content = content[header_end + 5:]
        
        tag_pattern = re.compile(r'<([A-Za-z_]+):(\d+)(?::[^>]*)?>([^<]*)', re.IGNORECASE)
        
        records = content.split('<EOR>')
        
        for record in records:
            if not record.strip():
                continue
                
            tags = {}
            for match in tag_pattern.finditer(record):
                tag_name = match.group(1).upper()
                tag_value = match.group(3).strip()
                tags[tag_name] = tag_value
            
            if 'CALL' in tags:
                try:
                    qso_date = None
                    time_on = None
                    
                    if 'QSO_DATE' in tags:
                        qso_date = tags['QSO_DATE']
                        qso_date = ''.join(c for c in qso_date if c.isdigit())
                        
                    if 'TIME_ON' in tags:
                        time_on = tags['TIME_ON']
                        time_on = ''.join(c for c in time_on if c.isdigit())
                    
                    if not time_on and 'TIME_OFF' in tags:
                        time_on = tags['TIME_OFF']
                        time_on = ''.join(c for c in time_on if c.isdigit())
                    
                    if not qso_date or not time_on:
                        print(f"Puutteellinen aikatieto: {tags.get('CALL', 'UNKNOWN')}")
                        continue
                    
                    if len(qso_date) != 8:
                        print(f"Virheellinen QSO_DATE: {qso_date}")
                        continue
                    
                    if len(time_on) == 4:
                        time_on += '00'
                    elif len(time_on) == 6:
                        pass
                    else:
                        print(f"Virheellinen TIME_ON: {time_on}")
                        continue
                    
                    datetime_str = f"{qso_date} {time_on}"
                    timestamp = datetime.datetime.strptime(datetime_str, '%Y%m%d %H%M%S')
                    
                    band = tags.get('BAND', self.current_band).upper()
                    if band.endswith('M') and band[:-1].isdigit():
                        band = band[:-1] + 'm'
                    elif band.endswith('CM') and band[:-2].isdigit():
                        band = band[:-2] + 'cm'
                    
                    mode = tags.get('MODE', self.current_mode).upper()
                    mode_map = {
                        'SSB': 'SSB', 'LSB': 'LSB', 'USB': 'USB', 'CW': 'CW', 
                        'FM': 'FM', 'AM': 'AM', 'FT8': 'FT8', 'FT4': 'FT4',
                        'RTTY': 'RTTY', 'PSK': 'PSK', 'JT65': 'JT65'
                    }
                    mode = mode_map.get(mode, mode)
                    
                    rst_sent = tags.get('RST_SENT', self.settings['default_rst_sent'])
                    rst_rcvd = tags.get('RST_RCVD', self.settings['default_rst_rcvd'])
                    
                    if not rst_sent or rst_sent == '0':
                        rst_sent = self.settings['default_rst_sent']
                    if not rst_rcvd or rst_rcvd == '0':
                        rst_rcvd = self.settings['default_rst_rcvd']
                    
                    comment = tags.get('COMMENT', '')
                    if not comment:
                        comment = tags.get('QSLMSG', tags.get('REMARKS', tags.get('NOTES', '')))
                    
                    my_gridsquare = tags.get('MY_GRIDSQUARE', '')
                    
                    # Etsi vasta-aseman WWFF-tunnus
                    their_wwff = ""
                    if 'SIG_INFO' in tags and tags.get('SIG') == 'WWFF':
                        their_wwff = tags['SIG_INFO']
                    
                    qso_data = {
                        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                        'call': tags['CALL'],
                        'band': band,
                        'mode': mode,
                        'rst_sent': rst_sent,
                        'rst_rcvd': rst_rcvd,
                        'comment': comment,
                        'my_gridsquare': my_gridsquare,
                        'their_wwff': their_wwff
                    }
                    
                    self.log_entries.append(qso_data)
                    success_count += 1
                    
                except Exception as e:
                    print(f"Virhe QSO:n jäsentämisessä: {e}")
                    print(f"Tags: {tags}")
                    continue
        
        return success_count
    
    def save_current_log(self):
        """Tallenna nykyinen loki"""
        if not self.current_log_file:
            self.save_log_as()
        else:
            self.save_to_file(self.current_log_file)
    
    def save_log_as(self):
        """Tallenna loki nimellä"""
        if self.settings['mywwff']:
            default_name = f"{self.settings['mycall'].replace('/', '_')}@{self.settings['mywwff']}.adi"
        elif self.settings['mylocator']:
            default_name = f"{self.settings['mycall'].replace('/', '_')}@{self.settings['mylocator']}.adi"
        else:
            default_name = f"{self.settings['mycall'].replace('/', '_')}.adi"
        
        filename = filedialog.asksaveasfilename(
            initialdir=self.settings['data_dir'],
            initialfile=default_name,
            defaultextension=".adi",
            filetypes=[("ADI files", "*.adi"), ("All files", "*.*")]
        )
        
        if filename:
            self.save_to_file(filename)
            self.current_log_file = filename
            self.log_modified = False
            self.update_header()
    
    def save_to_file(self, filename):
        """Tallenna ADI-muotoiseen tiedostoon"""
        try:
            adi_content = self.generate_adi()
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(adi_content)
            messagebox.showinfo("Tallennettu", f"Loki tallennettu: {filename}")
        except Exception as e:
            messagebox.showerror(self.texts['file_save_error'], f"Tallennus epäonnistui: {str(e)}")
    
    def generate_adi(self):
        """Luo ADI-muotoinen sisältö"""
        adi_content = []
        
        adi_content.append("<ADIF_VER:5>3.1.0")
        adi_content.append("<CREATED_TIMESTAMP:15>%s" % datetime.datetime.now().strftime('%Y%m%d %H%M%S'))
        adi_content.append("<PROGRAMID:7>HamLogger")
        adi_content.append("<PROGRAMVERSION:5>1.0.0")
        adi_content.append("<EOH>")
        
        for qso in self.log_entries:
            qso_date = datetime.datetime.strptime(qso['timestamp'], '%Y-%m-%d %H:%M:%S')
            
            record = []
            record.append(f"<STATION_CALLSIGN:{len(self.settings['mycall'])}>{self.settings['mycall']}")
            record.append(f"<CALL:{len(qso['call'])}>{qso['call']}")
            record.append(f"<QSO_DATE:8>{qso_date.strftime('%Y%m%d')}")
            record.append(f"<TIME_ON:6>{qso_date.strftime('%H%M%S')}")
            record.append(f"<BAND:{len(qso['band'])}>{qso['band']}")
            record.append(f"<MODE:{len(qso['mode'])}>{qso['mode']}")
            record.append(f"<RST_SENT:{len(qso['rst_sent'])}>{qso['rst_sent']}")
            record.append(f"<RST_RCVD:{len(qso['rst_rcvd'])}>{qso['rst_rcvd']}")
            
            # Oma WWFF (MY_SIG_INFO)
            if self.settings['mywwff']:
                record.append(f"<MY_SIG:4>WWFF")
                record.append(f"<MY_SIG_INFO:{len(self.settings['mywwff'])}>{self.settings['mywwff']}")
            
            # Vasta-aseman WWFF (SIG ja SIG_INFO)
            if qso.get('their_wwff'):
                record.append(f"<SIG:4>WWFF")
                record.append(f"<SIG_INFO:{len(qso['their_wwff'])}>{qso['their_wwff']}")
            
            if qso.get('my_gridsquare'):
                record.append(f"<MY_GRIDSQUARE:{len(qso['my_gridsquare'])}>{qso['my_gridsquare']}")
            
            if qso['comment']:
                record.append(f"<COMMENT:{len(qso['comment'])}>{qso['comment']}")
            
            record.append(f"<OPERATOR:{len(self.settings['mycall'])}>{self.settings['mycall']}")
            
            adi_content.extend(record)
            adi_content.append("<EOR>")
        
        return "\n".join(adi_content)
    
    def save_adi_dialog(self):
        """Tallenna ADI-tiedosto"""
        if not self.log_entries:
            messagebox.showwarning(self.texts['no_data'], "Ei tallennettavia QSO:ita")
            return
        
        if self.settings['mywwff']:
            default_name = f"{self.settings['mycall'].replace('/', '_')}@{self.settings['mywwff']}.adi"
        elif self.settings['mylocator']:
            default_name = f"{self.settings['mycall'].replace('/', '_')}@{self.settings['mylocator']}.adi"
        else:
            default_name = f"{self.settings['mycall'].replace('/', '_')}.adi"
        
        filename = filedialog.asksaveasfilename(
            initialdir=self.settings['data_dir'],
            initialfile=default_name,
            defaultextension=".adi",
            filetypes=[("ADI files", "*.adi"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                adi_content = self.generate_adi()
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(adi_content)
                messagebox.showinfo("Tallennettu", f"ADI-tiedosto tallennettu: {filename}")
            except Exception as e:
                messagebox.showerror(self.texts['file_save_error'], f"Tallennus epäonnistui: {str(e)}")
    
    def export_partial_log(self):
        """Vie osa lokista uudeksi lokiksi"""
        if not self.log_entries:
            messagebox.showwarning(self.texts['no_data'], "Ei vientiin kelpaavaa QSO-dataa")
            return
        
        export_window = tk.Toplevel(self.root)
        export_window.title(self.texts['export_partial'])
        export_window.geometry("400x200")
        
        ttk.Label(export_window, text="Valitse viennin ajankohdat:").pack(pady=10)
        
        date_frame = ttk.Frame(export_window)
        date_frame.pack(pady=10)
        
        ttk.Label(date_frame, text="Alkaen (pp.kk.vvvv):").grid(row=0, column=0, padx=5, pady=5)
        start_date_entry = ttk.Entry(date_frame, width=12)
        start_date_entry.grid(row=0, column=1, padx=5, pady=5)
        start_date_entry.insert(0, datetime.datetime.now().strftime('%d.%m.%Y'))
        
        ttk.Label(date_frame, text="Päättyen (pp.kk.vvvv):").grid(row=1, column=0, padx=5, pady=5)
        end_date_entry = ttk.Entry(date_frame, width=12)
        end_date_entry.grid(row=1, column=1, padx=5, pady=5)
        end_date_entry.insert(0, datetime.datetime.now().strftime('%d.%m.%Y'))
        
        def perform_export():
            try:
                start_date_str = start_date_entry.get().strip()
                end_date_str = end_date_entry.get().strip()
                
                start_date = datetime.datetime.strptime(start_date_str, '%d.%m.%Y')
                end_date = datetime.datetime.strptime(end_date_str, '%d.%m.%Y')
                end_date = end_date + datetime.timedelta(days=1)
                
                filtered_qsos = []
                for qso in self.log_entries:
                    qso_date = datetime.datetime.strptime(qso['timestamp'], '%Y-%m-%d %H:%M:%S')
                    if start_date <= qso_date < end_date:
                        filtered_qsos.append(qso)
                
                if not filtered_qsos:
                    messagebox.showwarning(self.texts['no_data'], f"Valitulla aikavälillä ({start_date_str} - {end_date_str}) ei löytynyt QSO:ita")
                    return
                
                if self.settings['mywwff']:
                    default_name = f"{self.settings['mycall'].replace('/', '_')}@{self.settings['mywwff']}_{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}.adi"
                elif self.settings['mylocator']:
                    default_name = f"{self.settings['mycall'].replace('/', '_')}@{self.settings['mylocator']}_{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}.adi"
                else:
                    default_name = f"{self.settings['mycall'].replace('/', '_')}_{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}.adi"
                
                filename = filedialog.asksaveasfilename(
                    initialdir=self.settings['data_dir'],
                    initialfile=default_name,
                    defaultextension=".adi",
                    filetypes=[("ADI files", "*.adi"), ("All files", "*.*")]
                )
                
                if filename:
                    original_entries = self.log_entries
                    self.log_entries = filtered_qsos
                    
                    try:
                        adi_content = self.generate_adi()
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(adi_content)
                        messagebox.showinfo(self.texts['export_complete'], f"Lokin osa tallennettu: {filename}\n{len(filtered_qsos)} QSO:ta")
                    finally:
                        self.log_entries = original_entries
                    
                    export_window.destroy()
                
            except ValueError as e:
                messagebox.showerror("Virheellinen päivämäärä", "Tarkista päivämäärän muoto (pp.kk.vvvv)")
            except Exception as e:
                messagebox.showerror("Viennin virhe", f"Vienti epäonnistui: {str(e)}")
        
        ttk.Button(export_window, text="Vie valittu osa", command=perform_export).pack(pady=10)
    
    def save_and_exit(self):
        """Tallenna ja sulje"""
        if self.log_modified:
            response = messagebox.askyesnocancel(
                self.texts['save_changes'],
                f"{self.texts['save_changes_question']} sulkemista?"
            )
            if response is None:
                return
            elif response:
                self.save_current_log()
        
        self.root.quit()
    
    def quit_application(self):
        """Sovelluksen sulkeminen"""
        self.save_and_exit()
    
    def edit_settings(self):
        """Muokkaa asetuksia"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title(self.texts['station_info'])
        settings_window.geometry("400x400")
        
        ttk.Label(settings_window, text="Oma kutsu:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        mycall_entry = ttk.Entry(settings_window, width=15)
        mycall_entry.insert(0, self.settings['mycall'])
        mycall_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(settings_window, text="Locator:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        locator_entry = ttk.Entry(settings_window, width=10)
        locator_entry.insert(0, self.settings['mylocator'])
        locator_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(settings_window, text="Oma WWFF:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        wwff_entry = ttk.Entry(settings_window, width=15)
        wwff_entry.insert(0, self.settings['mywwff'])
        wwff_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(settings_window, text="Oletusband:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        band_entry = ttk.Entry(settings_window, width=10)
        band_entry.insert(0, self.settings['default_band'])
        band_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(settings_window, text="Oletusmode:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        mode_entry = ttk.Entry(settings_window, width=10)
        mode_entry.insert(0, self.settings['default_mode'])
        mode_entry.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(settings_window, text="Teema:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        theme_var = tk.StringVar(value=self.settings.get('theme', 'oletus'))
        theme_combo = ttk.Combobox(settings_window, textvariable=theme_var, width=15, state="readonly")
        theme_combo['values'] = ('oletus', 'syksyinen metsä', 'suomi', 'yömodi', 'meri', 'kulta', 'joulu', 'retro', 'elegantti')
        theme_combo.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Kieli-valinta
        ttk.Label(settings_window, text="Kieli:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        language_var = tk.StringVar(value=self.settings.get('language', 'suomi'))
        language_combo = ttk.Combobox(settings_window, textvariable=language_var, width=15, state="readonly")
        language_combo['values'] = ('suomi', 'english')
        language_combo.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        
        def save_new_settings():
            self.settings['mycall'] = mycall_entry.get().strip()
            self.settings['mylocator'] = locator_entry.get().strip().upper()
            self.settings['mywwff'] = wwff_entry.get().strip().upper()
            self.settings['default_band'] = band_entry.get().strip()
            self.settings['default_mode'] = mode_entry.get().strip().upper()
            
            # Tallenna uudet asetukset
            old_theme = self.settings.get('theme', 'oletus')
            old_language = self.settings.get('language', 'suomi')
            
            self.settings['theme'] = theme_var.get()
            self.settings['language'] = language_var.get()
            
            self.current_band = self.settings['default_band']
            self.current_mode = self.settings['default_mode']
            self.language = self.settings['language']
            
            self.save_settings()
            self.update_info_display()
            
            # Päivitä teema ja kieli vain jos ne muuttuivat
            if old_theme != self.settings['theme']:
                self.apply_theme()
            
            if old_language != self.settings['language']:
                self.update_language()  # Tämä kutsuu update_ui_texts() automaattisesti
            
            settings_window.destroy()
            
            messagebox.showinfo("Asetukset tallennettu", "Asetukset on tallennettu onnistuneesti!")
        
        ttk.Button(settings_window, text="Tallenna", command=save_new_settings).grid(row=7, column=0, columnspan=2, pady=10)

def main():
    root = tk.Tk()
    app = HamLogger(root)
    root.mainloop()

if __name__ == "__main__":
    main()