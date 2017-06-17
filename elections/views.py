import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from elections.models import *

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


def name_to_href(str):
    # ltrPL = "ŻÓŁĆĘŚĄŹŃżółćęśąźń "
    # ltrnoPL = "ZOLCESAZNzolcesazn-"
    #
    # trantab = str.maketrans(ltrPL, ltrnoPL)
    #
    # str = str.translate(trantab)
    # str = str.lower()

    return str


@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
@csrf_exempt
def update_community(request):
    items = request._data

    args = items['name'].split('_')
    comms = Community.objects.all().filter(name=args[0]).filter(ancestor__name=args[1])
    comm_prev = comms[0]

    comm = Community(ancestor=comm_prev.ancestor, name=args[0],
                     votes_invalid=items["glosow_niewaznych"],
                     votes_valid=items["glosow_waznych"],
                     votes_cast=items["glosow_waznych"] + items["glosow_niewaznych"],
                     entitled_to_vote=items["uprawnionych"],
                     ballots_issued=items["kart_waznych"]
                     )

    results_ids_to_delete = []
    results_in_comms = ResultsInCommunity.objects.all().filter(community=comm_prev)
    for res in results_in_comms:
        cand_name = res.candidate.first_name + ' ' + res.candidate.last_name
        if cand_name not in items.keys():
            return HttpResponse(status=400)
        if items[cand_name] is None or int(items[cand_name]) < 0:
            return HttpResponse(status=400)

    comm.save()
    for res in results_in_comms:
        cand_name = res.candidate.first_name + ' ' + res.candidate.last_name
        new_res = ResultsInCommunity(community=comm, candidate=res.candidate, result=items[cand_name])
        results_ids_to_delete.append(res.id)
        new_res.save()

    for res_id in results_ids_to_delete:
        ResultsInCommunity.objects.all().filter(id=res_id).delete()

    Community.objects.all().filter(id=comm_prev.id).delete()
    return HttpResponse(status=200)


@csrf_exempt
def process_login(request):
    items = json.loads(request.body.decode("utf-8"))

    username = items['username']
    password = items['password']
    user = authenticate(username=username, password=password)
    if user is None:
        result = {
            'status': 'failure',
            'message': 'Niepoprawne dane logowania'
        }
        return JsonResponse(result, safe=False)

    # login(request, user)
    token = Token.objects.get_or_create(user=user)

    result = {
        'status': 'success',
        'token': token[0].key
    }
    return JsonResponse(result, safe=False)


@csrf_exempt
def process_signup(request):
    items = json.loads(request.body.decode("utf-8"))
    username = items['username']
    password = items['password']
    users = User.objects.filter(username=username)

    if len(users) != 0:
        result = {
            'status': 'failure',
            'message': 'Podany użytkownik już istnieje'
        }
        return JsonResponse(result, safe=False)

    user = User.objects.create_user(username, password=password)
    user.save()

    token = Token.objects.get_or_create(user=user)
    token = token[0]

    result = {
        'status': 'success',
        'token': token.key
    }
    return JsonResponse(result, safe=False)


def get_electoral_unit(name):
    if '_' in name:
        args = name.split('_')
        objects = Community.objects.all().filter(name=args[0]).filter(ancestor__name=args[1])
        type = Community
    elif name == '':
        objects = Country.objects.all().filter(name='Polska')
        type = Country
    elif name in [name_to_href(Province.objects.all()[i].name) for i in range(0, len(Province.objects.all()))]:
        objects = Province.objects.all().filter(name=name)
        type = Province
    else:
        type = Circuit
        objects = Circuit.objects.all().filter(name=name)
    return objects[0], type


def get_general_info(request, arg):
    electoral_unit, unit_type = get_electoral_unit(arg)
    general_info = electoral_unit.general()

    data = [
        {
            'label': 'Liczba uprawnionych do głosowania',
            'short': 'uprawnionych',
            'value': general_info['entitled_to_vote']
        },
        {
            'label': 'Liczba kart ważnych',
            'short': 'kart_waznych',
            'value': general_info['ballots_issued']
        },
        {
            'label': 'Liczba głosów ważnych',
            'short': 'glosow_waznych',
            'value': general_info['votes_valid']
        },
        {
            'label': 'Liczba głosów nieważnych',
            'short': 'glosow_niewaznych',
            'value': general_info['votes_invalid']
        },
    ]
    return JsonResponse(data, safe=False)


def get_candidates_info(request, arg):
    electoral_unit, unit_type = get_electoral_unit(arg)

    general_info = electoral_unit.general()
    candidates_results = electoral_unit.results()
    valid_votes = general_info['votes_valid']

    cand_table_data = []

    i = 0
    for res in candidates_results:
        name = res.first_name + ' ' + res.last_name
        if res.result is None:
            votes = 0
        else:
            votes = res.result

        support_val = 100 * votes / valid_votes
        if support_val > 100:
            support_val = 100
        support = ('%.2f' % support_val).replace(',', '.')

        cand_table_data.append([name, votes, support, colors[i]])
        i += 1

    general_labels = ['Lp', 'Imię i nazwisko', 'Liczba oddanych głosów', 'Wynik wyborczy']
    data = {'cand_table': sorted(cand_table_data, key=lambda x: x[1], reverse=True),
            'labels': general_labels}
    return JsonResponse(data, safe=False)


def get_detailed_info(request, arg):
    electoral_unit, unit_type = get_electoral_unit(arg)

    descendants = []

    if unit_type == Country:
        descendants = Province.objects.all()
    elif unit_type == Province:
        descendants = electoral_unit.circuit_set.all()
    elif unit_type == Circuit:
        descendants = electoral_unit.community_set.all()

    detailed_results = []

    cand_names = []

    fill_labels = True
    for descendant in descendants:
        desc_res = descendant.results()
        name = descendant.name

        if name.isdigit() and len(name) == 1:
            name = '0' + name

        if descendant.name.isdigit():
            name = 'Obwód' + name

        href = '?name=' + name_to_href(name)

        if unit_type == Circuit:
            href += '_' + descendant.ancestor.name + '&is_community=true'
        else:
            href += '&is_community=false'

        desc_data = [href, name, descendant.general()['votes_valid']]
        for res in desc_res:
            votes = res.result
            desc_data.append(votes)

            if fill_labels is True:
                name = res.first_name + ' ' + res.last_name
                cand_names.append(name)

        fill_labels = False
        detailed_results.append(desc_data)
        labels = ['Nazwa jednostki', 'Głosy ważne'] + cand_names

        data = {
            'labels': labels,
            'detailed_results': sorted(detailed_results, key=lambda x: x[1]),
        }

    return JsonResponse(data, safe=False)


def get_search_results(request, arg):
    if arg is '':
        return JsonResponse({}, safe=False)

    cand_names = []

    country = Country.objects.all()[0]
    cres = country.results()

    for res in cres:
        cand_names.append(res.first_name + ' ' + res.last_name)

    labels = ['Nazwa jednostki', 'Głosy ważne'] + cand_names

    comm_name = arg
    comms = Community.objects.all().filter(name__contains=comm_name)

    detailed_results = []

    for comm in comms:
        desc_res = comm.results()
        name = comm.name

        href = '?name=' + name_to_href(name)
        href += '_' + comm.ancestor.name + '&is_community=true'

        desc_data = [href, name, comm.general()['votes_valid']]
        for res in desc_res:
            votes = res.result
            desc_data.append(votes)

        detailed_results.append(desc_data)

    data = {
        'labels': labels,
        'detailed_results': sorted(detailed_results, key=lambda x: x[1])
    }

    return JsonResponse(data, safe=False)
