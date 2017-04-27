# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum
from django.db import transaction


class ElectoralUnit():
    def descendants(self):
        return []

    @transaction.atomic
    def results_from_descendants(self):
        return list(map(lambda res: (res, res.results()), self.descendants()))

    def __unicode(self):
        return self.__str__().encode('utf-8')


class Province(models.Model):
    pass


class Circuit(models.Model):
    pass


class Community(models.Model):
    pass


class Candidate(models.Model):
    first_name = models.CharField(max_length=32, editable=False)
    last_name = models.CharField(max_length=32)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Country(models.Model, ElectoralUnit):
    name = models.CharField(max_length=32)

    @transaction.atomic
    def results(self):
        return Candidate.objects.all().annotate(result=Sum('resultsincommunity__result'))

    def descendants(self):
        return Province.objects.all()

    def general(self):
        return Community.objects.all().aggregate(
            votes_invalid=Sum('votes_invalid'),
            votes_cast=Sum('votes_cast'),
            votes_valid=Sum('votes_valid'),
            entitled_to_vote=Sum('entitled_to_vote'),
            ballots_issued=Sum('ballots_issued')
        )


class Province(models.Model, ElectoralUnit):
    name = models.CharField(max_length=32)

    def __str__(self):
        return "Województwo " + self.name

    @transaction.atomic
    def results(self):
        return Candidate.objects.filter(resultsincommunity__community__ancestor__ancestor=self). \
            annotate(result=Sum('resultsincommunity__result'))

    def descendants(self):
        return Circuit.objects.filter(ancestor=self)

    def general(self):
        return Community.objects.filter(ancestor__ancestor=self).aggregate(
            votes_invalid=Sum('votes_invalid'),
            votes_cast=Sum('votes_cast'),
            votes_valid=Sum('votes_valid'),
            entitled_to_vote=Sum('entitled_to_vote'),
            ballots_issued=Sum('ballots_issued')
        )


class Circuit(models.Model, ElectoralUnit):
    ancestor = models.ForeignKey(Province, on_delete=models.CASCADE, editable=False)
    name = models.CharField(editable=False, max_length=32)
    desc = models.CharField(max_length=128)

    def __str__(self):
        return "Okręg " + str(self.name)

    @transaction.atomic
    def results(self):
        return Candidate.objects.filter(resultsincommunity__community__ancestor=self). \
            annotate(result=Sum('resultsincommunity__result'))

    def descendants(self):
        return Community.objects.filter(ancestor=self)

    def general(self):
        return Community.objects.filter(ancestor=self).aggregate(
            votes_invalid=Sum('votes_invalid'),
            votes_cast=Sum('votes_cast'),
            votes_valid=Sum('votes_valid'),
            entitled_to_vote=Sum('entitled_to_vote'),
            ballots_issued=Sum('ballots_issued')
        )


class Community(models.Model, ElectoralUnit):
    ancestor = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)

    votes_invalid = models.IntegerField()
    votes_cast = models.IntegerField()
    votes_valid = models.IntegerField()
    entitled_to_vote = models.IntegerField()
    ballots_issued = models.IntegerField()

    def __str__(self):
        return "Gmina " + self.name

    @transaction.atomic
    def results(self):
        return Candidate.objects.filter(resultsincommunity__community=self). \
            annotate(result=Sum('resultsincommunity__result'))

    def general(self):
        return {
            "votes_invalid": self.votes_invalid,
            "votes_cast": self.votes_cast,
            "votes_valid": self.votes_valid,
            "entitled_to_vote": self.entitled_to_vote,
            "ballots_issued": self.ballots_issued
        }


class ResultsInCommunity(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, editable=False)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, editable=False)

    result = models.IntegerField()

    def __str__(self):
        return 'Kandydat: {}, Gmina: {}. Okręg: {}, Województwo: {}'. \
            format(self.candidate,
                   self.community,
                   self.community.ancestor,
                   self.community.ancestor.ancestor
                   ).encode('ascii', errors='replace')
