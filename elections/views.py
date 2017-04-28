from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from elections.models import *
from elections.my_forms import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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


def process_search(request):
    data = {
        'input_value': '',
        'query_sent': False,
        'czy_zalogowany': request.user.is_authenticated()
    }
    if request.method == 'POST':
        form = SearchForm(data=request.POST)
        if form.is_valid():
            cand_names = []

            country = Country.objects.all()[0]
            cres = country.results()

            for res in cres:
                cand_names.append(res.first_name + ' ' + res.last_name)

            labels = ['Nazwa jednostki', 'Głosy ważne'] + cand_names

            comm_name = form['community'].value()
            comms = Community.objects.all().filter(name__contains=comm_name)

            detailed_results = []

            for comm in comms:
                desc_res = comm.results()
                name = comm.name

                href = '/wyniki/' + name_to_href(name) + '_' + comm.ancestor.name
                desc_data = [href, name, comm.general()['votes_valid']]
                for res in desc_res:
                    votes = res.result
                    desc_data.append(votes)

                detailed_results.append(desc_data)

            data = {
                'labels': labels,
                'wyniki': sorted(detailed_results, key=lambda x: x[1]),
                'input_value': comm_name,
                'query_sent': True,
                'czy_zalogowany': request.user.is_authenticated()
            }

    return render(request, "search.html", data)


def get_webpage_data(class_type, name):
    if class_type == Community:
        args = name.split('_')
        objects = class_type.objects.all().filter(name=args[0]).filter(ancestor__name=args[1])
    else:
        objects = class_type.objects.all().filter(name=name)

    electoral_unit = objects[0]
    general_info = electoral_unit.general()

    candidates_results = electoral_unit.results()

    valid_votes = general_info['votes_valid']

    cand_table_data = []
    cand_names = []

    i = 0
    for res in candidates_results:
        name = res.first_name + ' ' + res.last_name
        votes = res.result
        support_val = 100 * res.result / valid_votes
        if support_val > 100:
            support_val = 100
        support = ('%.2f' % support_val).replace(',', '.')

        cand_names.append(name)
        cand_table_data.append([name, votes, support, colors[i]])
        i += 1

    labels = ['Nazwa jednostki', 'Głosy ważne'] + cand_names

    descendants = []

    if class_type == Country:
        descendants = Province.objects.all()
    elif class_type == Province:
        descendants = electoral_unit.circuit_set.all()
    elif class_type == Circuit:
        descendants = electoral_unit.community_set.all()

    detailed_results = []

    hierarchy_nodes = []

    if class_type != Country:
        node = electoral_unit
        name = node.name

        if name.isdigit() and len(name) == 1:
            name = '0' + name

        if name.isdigit():
            name = 'Obwód' + name
        hierarchy_nodes.append(name)

        while type(node) != Province:
            node = node.ancestor
            name = node.name
            if name.isdigit() and len(name) == 1:
                name = '0' + name

            if name.isdigit():
                name = 'Obwód' + name
            hierarchy_nodes.append(name)

    for descendant in descendants:
        desc_res = descendant.results()
        name = descendant.name

        if name.isdigit() and len(name) == 1:
            name = '0' + name

        if descendant.name.isdigit():
            name = 'Obwód' + name

        href = '/wyniki/' + name_to_href(name)

        if class_type == Circuit:
            href += '_' + descendant.ancestor.name

        desc_data = [href, name, descendant.general()['votes_valid']]
        for res in desc_res:
            votes = res.result
            desc_data.append(votes)

        detailed_results.append(desc_data)

    data = {
        'czy_gmina': class_type == Community,
        'uprawnionych': general_info['entitled_to_vote'],
        'kart_waznych': general_info['ballots_issued'],
        'glosow_waznych': general_info['votes_valid'],
        'glosow_niewaznych': general_info['votes_invalid'],
        'kandydaci': sorted(cand_table_data, key=lambda x: x[1], reverse=True),
        'labels': labels,
        'wyniki': sorted(detailed_results, key=lambda x: x[1]),
        'jednostki': reversed(hierarchy_nodes)
    }

    return data


def index(request, arg):
    arg = arg.replace('.html', '')
    if arg == '':
        data = get_webpage_data(Country, 'Polska')
    elif arg in [name_to_href(Province.objects.all()[i].name) for i in range(0, len(Province.objects.all()))]:
        data = get_webpage_data(Province, arg)
    elif arg in [name_to_href(Circuit.objects.all()[i].name) for i in range(0, len(Circuit.objects.all()))]:
        data = get_webpage_data(Circuit, arg)
    else:
        if request.method == 'POST':
            update_community(request, arg)
        data = get_webpage_data(Community, arg)

    is_logged = request.user.is_authenticated()

    data.update(czy_zalogowany=is_logged)

    return render(request, "subpage.html", data)


def update_community(request, comm_name):
    cands = Candidate.objects.all()
    cands_names = [candidate.first_name + ' ' + candidate.last_name for candidate in cands]
    stats = [
        'uprawnionych',
        'kart_waznych',
        'glosow_waznych',
        'glosow_niewaznych'
    ]

    labels = stats + cands_names

    form = UpdateForm(labels, request.POST)
    if form.is_valid():
        args = comm_name.split('_')
        comms = Community.objects.all().filter(name=args[0]).filter(ancestor__name=args[1])
        comm_prev = comms[0]

        comm = Community(ancestor=comm_prev.ancestor, name=args[0],
                         votes_invalid=form["glosow_niewaznych"].value(),
                         votes_valid=form["glosow_waznych"].value(),
                         votes_cast=form["glosow_waznych"].value() + form["glosow_niewaznych"].value(),
                         entitled_to_vote=form["uprawnionych"].value(),
                         ballots_issued=form["kart_waznych"].value()
                         )
        comm.save()

        results_ids_to_delete = []
        results_in_comms = ResultsInCommunity.objects.all().filter(community=comm_prev)
        for res in results_in_comms:
            cand_name = res.candidate.first_name + ' ' + res.candidate.last_name
            new_res = ResultsInCommunity(community=comm, candidate=res.candidate, result=form[cand_name].value())
            results_ids_to_delete.append(res.id)
            new_res.save()

        for res_id in results_ids_to_delete:
            ResultsInCommunity.objects.all().filter(id=res_id).delete()

        Community.objects.all().filter(id=comm_prev.id).delete()


def process_login_form(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form['username'].value()
            password = form['password'].value()
            request_path = form['request_path'].value()
            user = authenticate(username=username, password=password)
            if user is None:
                return render(request, 'login.html', {'form': RegisterForm(), 'msg': 'Niepoprawne dane logowania'})

            login(request, user)
            return redirect(request_path)

    else:
        form = LoginForm()
        data = {
            'form': form,
            'msg': '',
            'request_path': request.META.get('HTTP_REFERER', '/')
        }
        return render(request, 'login.html', data)


def process_signup_form(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            username = form['username'].value()
            password = form['password'].value()
            request_path = form['request_path'].value()
            users = User.objects.filter(username=username)
            if len(users) != 0:
                return render(request, 'signup.html',
                              {'form': RegisterForm(), 'msg': 'Użytkownik o podanym loginie już istnieje'})

            user = User.objects.create_user(username, password=password)
            user.save()
            login(request, user)
            return redirect(request_path)

    else:
        form = RegisterForm()
        data = {
            'form': form,
            'msg': '',
            'request_path': request.META.get('HTTP_REFERER', '/')
        }
        return render(request, 'signup.html', data)


def process_logout(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
