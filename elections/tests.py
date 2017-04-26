from django.test import TestCase
from elections.models import *


class TestCountry(TestCase):
    def setUp(self):
        w = Province.objects.create(name='Losowe')
        w.save()
        okr = Circuit.objects.create(province=w, name='testowy okręg1', desc='dd okręg1')
        okr.save()
        gm1 = Community.objects.create(circuit=okr, name='2137',
                                       votes_invalid=15,
                                       votes_cast=300,
                                       votes_valid=250,
                                       entitled_to_vote=1000,
                                       ballots_issued=310)
        gm1.save()
        gm2 = Community.objects.create(circuit=okr, name='2138',
                                       votes_invalid=152,
                                       votes_cast=3002,
                                       votes_valid=2502,
                                       entitled_to_vote=10002,
                                       ballots_issued=3102)
        gm2.save()

        k1 = Candidate.objects.create(first_name='TesterI', last_name='TesterN')
        k1.save()
        k2 = Candidate.objects.create(first_name='TesterDrugiI', last_name='TesterDrugiN')
        k2.save()

        w1_1 = ResultsInCommunity.objects.create(community=gm1, candidate=k1, result=15)
        w1_1.save()
        w1_2 = ResultsInCommunity.objects.create(community=gm2, candidate=k1, result=400)
        w1_2.save()
        w2_1 = ResultsInCommunity.objects.create(community=gm1, candidate=k2, result=23)
        w2_1.save()
        w2_2 = ResultsInCommunity.objects.create(community=gm2, candidate=k2, result=417)
        w2_2.save()

    def sprawdz_wyniki(self, obj, TesterIRes, TesterDrugiIRes):
        results = obj.results()
        self.assertEquals(len(results), 2)
        self.assertEquals({results[0].first_name, results[1].first_name}, {'TesterI', 'TesterDrugiI'})
        for result in results:
            if result.first_name == 'TesterI':
                self.assertEquals(result.result, TesterIRes)
            else:
                self.assertEquals(result.result, TesterDrugiIRes)

    def ogolny_test(self, obj_class, name, TesterIRes, TesterDrugiIRes):
        obj = obj_class.objects.filter(name=name)
        self.assertEquals(len(obj), 1)
        self.sprawdz_wyniki(obj[0], TesterIRes, TesterDrugiIRes)

    def test_gmina(self):
        self.ogolny_test(Community, 2137, 15, 23)

    def test_okreg(self):
        self.ogolny_test(Circuit, 'testowy okręg1', 415, 440)

    def test_wojewodztwo(self):
        self.ogolny_test(Province, 'Losowe', 415, 440)
