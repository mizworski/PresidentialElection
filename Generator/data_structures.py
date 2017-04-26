import os

kody_gmin = {}

wyniki_cale = {}
wyniki_woj = {}
wyniki_okregu = {}
wyniki_gminy = {}
wyniki_obw = {}

poziomy = ['Cała', 'Województwo', 'Okręg', 'Gmina', 'Obwód', ' ']
dane_poziomu = {
    'Cała': wyniki_cale,
    'Województwo': wyniki_woj,
    'Okręg': wyniki_okregu,
    'Gmina': wyniki_gminy,
    'Obwód': wyniki_obw,
    ' ': {}
}

DATA_FOLDER = 'data/'
TEMPLATES_FOLDER = 'templates/'
BASE_LINK = "0"  # relatywny link do strony domowej ( mapy polski )
FILES_LOCATION = ""  # lokalizacja plików ze stronami w systemie - podawana przez użytkownika
TABLE_TMPL_FILE = os.getcwd() + '/' + TEMPLATES_FOLDER + "/table_tmpl.js"
MAP_TMPL_FILE = os.getcwd() + '/' + TEMPLATES_FOLDER + "/map_tmpl.js"
HTML_TMPL_FILE = os.getcwd() + '/' + TEMPLATES_FOLDER + "/html_tmpl.html"
CSS_FILE = os.getcwd() + '/' + TEMPLATES_FOLDER + 'prezydent.css'
