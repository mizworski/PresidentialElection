#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import ResultsInCommunity, Province, Circuit, Community
from django.db import models
from django import forms


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class CommunityInline(admin.TabularInline):
    model = Community
    extra = 0
    can_delete = False
    # readonly_fields = ('name', 'votes_valid', 'ballots_issued')


@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    search_fields = ('name', 'ancestor__name')
    list_display = ('name', 'ancestor')
    inlines = (CommunityInline,)


class ResultsFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        super(ResultsFormset, self).clean()
        sum = 0
        # for form in self.forms:
        #     if form.cleaned_data['result'] < 0:
        #         raise forms.ValidationError(
        #             'Liczba głosów nie może być ujemna')
        #     sum += form.cleaned_data['result']
        # print(sum)

        # if sum > self.instance.result:
        #     raise forms.ValidationError(
        #         "Liczba głosów przekracza liczbę wydanych kart")
        # self.instance.result = sum
        self.instance.save()


class ResultsInline(admin.TabularInline):
    model = ResultsInCommunity
    can_delete = False
    extra = 0
    readonly_fields = ['candidate']
    search_fields = ('candidate',)
    list_display = ('candidate',)
    # formset = ResultsFormset


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    search_fields = ('name', 'ancestor__name')
    list_display = ('name', 'ancestor')
    readonly_fields = ('votes_valid',)
    inlines = [ResultsInline, ]

    # def save_model(self, request, obj, form, change):
    #     obwod = Community.objects.select_for_update().get(pk=obj.pk)
    #     super(CommunityAdmin, self).save_model(request, obj, form, change)
    #     # import time
    #     # time.sleep(5)

# @admin.register(ResultsInCommunity)
# class ResultsAdmin(admin.ModelAdmin):
#     fields = ["result"]
