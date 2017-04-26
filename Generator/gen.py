
#
# def insert_into_db():
#     for cand in wyniki_cale.keys():
#         if cand not in kolumny_ogolne:
#             dane = kand.rsplit(None, 1)
#             k = Kandydat(imie=dane[0], nazwisko=dane[1])
#             k.save()
#
#     for woj, wyn_okr in wyniki_obw.items():
#         w = Wojewodztwo(nazwa=woj)
#         w.save()
#
#         for okr, wyn_gm in wyn_okr.items():
#             o = Okreg(wojewodztwo=w, nazwa=int(okr))
#             o.save()
#
#             for gm, wyn_obw in wyn_gm.items():
#                 g = Gmina(okreg=o, nazwa=gm)
#                 g.save()
#
#                 for obw, wyn_w_obw in wyn_obw.items():
#                     ob = Obwod(gmina=g, nazwa=int(obw),
#                                glosy_niewazne=wyn_w_obw["Głosy nieważne"],
#                                glosy_oddane=wyn_w_obw["Głosy oddane"],
#                                glosy_wazne=wyn_w_obw["Głosy ważne"],
#                                uprawnieni=wyn_w_obw["Uprawnieni"],
#                                wydane_karty=wyn_w_obw["Wydane karty"]
#                                )
#                     ob.save()
#
#                     for kand_nazwa, wynik in wyn_w_obw.items():
#                         if kand_nazwa not in kolumny_ogolne:
#                             kandydat = Kandydat.objects.get(nazwisko=kand_nazwa.rsplit(None, 1)[1])
#
#                             w_w_obw = WynikiWObwodzie(obwod=ob, kandydat=kandydat, wynik=wynik)
#                             w_w_obw.save()