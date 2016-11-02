#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from dwapi import datawiz
import tabledatawiz as tb
from django.core.cache import cache

import pandas as pd
import datetime


dw = datawiz.DW()

def client(request):
    return render(request,'table/client.html')

#Функція формує талицю товарі які піднялися або впали в продажах і повертає у вигдялі DataFrame


def table(request):
    date_to = datetime.date(2015, 11, 18)
    date_from = datetime.date(2015, 11, 17)

    if request.method == 'GET':
        quantity = request.GET['col']
        znak = request.GET['znak']
        #table = tb.table_plus_minus(date_from, date_to, znak)
        if znak == 'plus':
            key_table = 'key_table_plus'
        else:
            key_table = 'key_table_minus'
        if key_table in cache:
            #table = (cache.get(tb.table_plus_minus(date_from, date_to, znak).head(int(quantity))))
            table = (cache.get(key_table)).head(int(quantity))
        else:
            cache.set(key_table, tb.table_main(date_from, date_to))
            table = (cache.get(key_table)).head(int(quantity))
        #print znak
        #return HttpResponse(quantity)
        return HttpResponse(table.to_html(index=False))


    if request.method == "POST":

        name = request.POST['name']
        secret = request.POST['secret']
        dw = datawiz.DW(name, secret)
        client_info = dw.get_client_info()
        shops = []
        for shop in client_info['shops']:
            shops.append(client_info['shops'][shop])
            #100 * data[str(date_to)] / data[str(date_from)] - 100
        # назви стовпців в табиці
        if 'key_table_main' in cache:
            t_m = cache.get('key_table_main')
        else:
            cache.set('key_table_main',tb.table_main(date_from, date_to))
            t_m = cache.get('key_table_main')

        if 'key_table_minus' in cache:
            #table_minus = (cache.get(tb.table_plus_minus(date_from, date_to, 'minus').head(30)))
            table_minus = (cache.get('key_table_minus')).head(30)
        else:
            cache.set('key_table_minus', tb.table_plus_minus(date_from, date_to, 'minus'))
            table_minus = (cache.get('key_table_minus')).head(30)

        if 'key_table_plus' in cache:
            #table_plus = (cache.get(tb.table_plus_minus(date_from, date_to, 'plus').head(30)))
            table_plus = (cache.get('key_table_plus')).head(30)
        else:
            cache.set('key_table_plus', tb.table_plus_minus(date_from, date_to, 'plus'))
            table_plus = (cache.get('key_table_plus')).head(30)

        key = {'table_main':t_m.to_html(index=False), 'table_plus':table_plus.to_html(index=False), 'table_minus':table_minus.to_html(index=False), 'client_info':client_info, 'shops':shops}
        #return render(request, 'table/table.html')
        #key = {'table_plus':t_m.to_html(index=False)}
        return render(request, 'table/table.html', key)


