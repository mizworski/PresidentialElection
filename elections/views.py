from django.http import HttpResponse
from django.shortcuts import render
from elections.models import *
from django.template import Context
from django.db import models

poziomy = ["province", "circuit", "community", ""]
poziomy_id = ["province_id", "circuit_id", "community_id", ""]
klasy = [Province, Circuit, Community]

colors = [
    '#EEA2AD',
    '#B0171F',
    '#7A67EE',
    '#C6E2FF',
    '#00868B',
    '#00EE76',
    '#483D8B',
    '#8B8386',
    '#FF8C00',
    '#CD4F39',
    '#006400',
    '#800080'
]


def get_webpage_data(class_type, name):
    objects = class_type.objects.all().filter(name=name)
    object = objects[0]
    general_info = object.general()

    candidates_results = object.results()

    valid_votes = general_info['votes_valid']

    cand_table_data = []
    cand_names = []

    i = 0
    for res in candidates_results:
        name = res.first_name + ' ' + res.last_name
        votes = res.result
        support = ('%.2f' % (100 * res.result / valid_votes)).replace(',', '.')
        cand_names.append(name)
        cand_table_data.append([name, votes, support, colors[i]])
        i += 1

    labels = ['Nazwa jednostki', 'Głosy ważne'] + cand_names

    descendants = []

    if class_type == Country:
        descendants = Province.objects.all()
    elif class_type == Province:
        descendants = object.circuit_set.all()
    elif class_type == Circuit:
        descendants = object.communitys.all()

    detailed_results = []

    for descendant in descendants:
        desc_res = descendant.results()
        desc_data = [descendant.name, object.general()['votes_valid']]
        for res in desc_res:
            votes = res.result
            desc_data.append(votes)

        detailed_results.append(desc_data)

    data = {
        'uprawnionych': general_info['entitled_to_vote'],
        'kart_waznych': general_info['ballots_issued'],
        'glosow_waznych': general_info['votes_valid'],
        'glosow_niewaznych': general_info['votes_invalid'],
        'kandydaci': sorted(cand_table_data, key=lambda x: x[1], reverse=True),
        'labels': labels,
        'wyniki': detailed_results
    }

    return data


def index(request):
    data = get_webpage_data(Province, 'POMORSKIE')

    return render(request, "subpage.html", data)
