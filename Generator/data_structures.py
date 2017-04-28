import os

kody_gmin = {}

wyniki_cale = {}
wyniki_woj = {}
wyniki_okregu = {}
wyniki_gminy = {}
circuit_results = {}

poziomy = ['Cała', 'Województwo', 'Okręg', 'Gmina', 'Obwód', ' ']
dane_poziomu = {
    'Cała': wyniki_cale,
    'Województwo': wyniki_woj,
    'Okręg': wyniki_okregu,
    'Gmina': wyniki_gminy,
    'Obwód': circuit_results,
    ' ': {}
}

DATA_FOLDER = 'data/'
TEMPLATES_FOLDER = 'templates/'
BASE_LINK = "0"
FILES_LOCATION = ""
