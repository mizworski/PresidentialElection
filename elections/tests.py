from django.test import TestCase
from elections.models import *


class TestCountry(TestCase):
    def setUp(self):
        province = Province.objects.create(name='Losowe')
        province.save()
        circ = Circuit.objects.create(ancestor=province, name='testowy okręg1', desc='dd okręg1')
        circ.save()
        c1 = Community.objects.create(ancestor=circ, name='2137',
                                      votes_invalid=15,
                                      votes_cast=300,
                                      votes_valid=250,
                                      entitled_to_vote=1000,
                                      ballots_issued=310)
        c1.save()
        c2 = Community.objects.create(ancestor=circ, name='2138',
                                      votes_invalid=152,
                                      votes_cast=3002,
                                      votes_valid=2502,
                                      entitled_to_vote=10002,
                                      ballots_issued=3102)
        c2.save()

        cand1 = Candidate.objects.create(first_name='Janek', last_name='kmwtw')
        cand1.save()
        cand2 = Candidate.objects.create(first_name='Karol', last_name='Wu')
        cand2.save()

        w1_1 = ResultsInCommunity.objects.create(community=c1, candidate=cand1, result=15)
        w1_1.save()
        w1_2 = ResultsInCommunity.objects.create(community=c2, candidate=cand1, result=400)
        w1_2.save()
        w2_1 = ResultsInCommunity.objects.create(community=c1, candidate=cand2, result=23)
        w2_1.save()
        w2_2 = ResultsInCommunity.objects.create(community=c2, candidate=cand2, result=417)
        w2_2.save()

    def sprawdz_wyniki(self, obj, JanekRes, KarolRes):
        results = obj.results()
        self.assertEquals(len(results), 2)
        self.assertEquals({results[0].first_name, results[1].first_name}, {'Janek', 'Karol'})
        for result in results:
            if result.first_name == 'Janek':
                self.assertEquals(result.result, JanekRes)
            else:
                self.assertEquals(result.result, KarolRes)

    def ogolny_test(self, obj_class, name, JanekRes, KarolRes):
        obj = obj_class.objects.filter(name=name)
        self.assertEquals(len(obj), 1)
        self.sprawdz_wyniki(obj[0], JanekRes, KarolRes)

    def test_gmina(self):
        self.ogolny_test(Community, 2137, 15, 23)

    def test_okreg(self):
        self.ogolny_test(Circuit, 'testowy okręg1', 415, 440)

    def test_wojewodztwo(self):
        self.ogolny_test(Province, 'Losowe', 415, 440)
