#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

import jinja2
import os
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'AplikacjeWWW2.settings'
application = get_wsgi_application()

from Generator.utils import *
from Generator.data_structures import *
from elections.models import *

templateLoader = jinja2.FileSystemLoader(searchpath="/")
templateEnv = jinja2.Environment(loader=templateLoader)


def row_to_dicts_entries_keys(csv_row):
    """Parse csv and to dict entries in our format."""

    woj = csv_row['Województwo']
    nr_okregu = csv_row['Nr okręgu']
    nazwa_gminy = csv_row['Gmina']

    kody_gmin[nazwa_gminy] = csv_row['Kod gminy']

    ballots_issued = int(csv_row['Karty wydane'])

    for rec in ['Województwo', 'Nr okręgu', 'Kod gminy', 'Powiat', 'Obwody', 'Gmina', 'Karty wydane']:
        del csv_row[rec]

    for key, val in csv_row.items():
        csv_row[key] = int(val)

    set_in_dict(circuit_results, [woj, nr_okregu, nazwa_gminy], csv_row)
    set_in_dict(circuit_results, [woj, nr_okregu, nazwa_gminy, "Wydane karty"], ballots_issued)
    for key, val in csv_row.items():
        update_dict(wyniki_gminy, [woj, nr_okregu, nazwa_gminy, key], val)
        update_dict(wyniki_okregu, [woj, nr_okregu, key], val)
        update_dict(wyniki_woj, [woj, key], val)
        update_dict(wyniki_cale, [key], val)


def row_to_dicts_entries_values(woj, csv_row):
    nr_okregu = csv_row['Nr\nokr.']
    nazwa_gminy = csv_row['Gmina']

    for rec in ['Adres', 'Nr okręgu', 'Kod\ngminy', 'Powiat', 'Nr\nobw.', 'Gmina', 'Typ\nobw.']:
        del csv_row[rec]

    for key, val in csv_row.items():
        csv_row[key] = int(val)

    set_in_dict(circuit_results, [woj, nr_okregu, nazwa_gminy], csv_row)

    for key, val in csv_row.items():
        update_dict(wyniki_gminy, [woj, nr_okregu, nazwa_gminy, key], val)
        update_dict(wyniki_okregu, [woj, nr_okregu, key], val)
        update_dict(wyniki_woj, [woj, key], val)
        update_dict(wyniki_cale, [key], val)


general_data_cols = ["Głosy nieważne", "Głosy oddane", "Głosy ważne", "Uprawnieni", "Wydane karty"]


def insert_into_db():
    polska = Country(name='Polska')
    polska.save()

    for col_label in wyniki_cale.keys():
        if col_label not in general_data_cols:
            entry = col_label.rsplit(None, 1)
            candidate = Candidate(first_name=entry[0], last_name=entry[1])
            candidate.save()

    for province, circuit_res in circuit_results.items():
        province = Province(name=province)
        province.save()

        for circuit, community_res in circuit_res.items():
            circuit = Circuit(ancestor=province, name=circuit)
            circuit.save()

            for community, cand_res_in_comm in community_res.items():
                comm = Community(ancestor=circuit, name=community,
                                 votes_invalid=cand_res_in_comm["Głosy nieważne"],
                                 votes_cast=cand_res_in_comm["Głosy oddane"],
                                 votes_valid=cand_res_in_comm["Głosy ważne"],
                                 entitled_to_vote=cand_res_in_comm["Uprawnieni"],
                                 ballots_issued=cand_res_in_comm["Wydane karty"]
                                 )
                comm.save()

                for cand, wynik in cand_res_in_comm.items():
                    if cand not in general_data_cols:
                        candidate = Candidate.objects.get(last_name=cand.rsplit(None, 1)[1])

                        res_in_comm = ResultsInCommunity(community=comm, candidate=candidate, result=wynik)
                        res_in_comm.save()


with open('data/pkw2000.csv') as csvfile:
    results = csv.DictReader(csvfile)

    for row in results:
        row_to_dicts_entries_keys(row)

    insert_into_db()
