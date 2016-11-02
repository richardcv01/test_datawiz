#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dwapi import datawiz

import datetime

from pandas import Series, DataFrame
import pandas as pd

dw = datawiz.DW()


def table_main(date_from, date_to):
    oborot =  dw.get_categories_sale(date_from=date_from, date_to=date_to).sum(axis=1)
    category = dw.get_categories_sale(by = "qty", date_from=date_from, date_to=date_to).sum(axis=1)
    receipts = dw.get_categories_sale(categories = ['sum'], by = "receipts_qty", date_from=date_from, date_to=date_to).T
    receipts = receipts[receipts.index == 'sum']
    mean_receipts = oborot / receipts

    frame = DataFrame()
    frame = frame.append(oborot, ignore_index=True)
    frame = frame.append(category, ignore_index=True)
    frame = frame.append(receipts, ignore_index=True)
    frame = frame.append(mean_receipts, ignore_index=True)
    frame.columns =[date_from, date_to]

    frame['Показник'] = ['Оборот', 'Кількість товарів', 'Кількість чеків', 'Середній чек']
    frame = frame[['Показник',date_to, date_from]]
    frame['Різниця у %'] = ((frame[date_to] - frame[date_from])/frame[date_from]) * 100
    frame['Різниця'] = frame[date_to] - frame[date_from]
    return frame

def table_plus_minus(date_from, date_to, plus_minus):
    name_to_turnover = str(date_to) + '_turnover'
    name_from_turnover = str(date_from) + '_turnover'
    name_to_qtr = str(date_to) + '_qty'
    name_from_qtr = str(date_from) + '_qty'

    data_oborot = dw.get_products_sale(by='turnover', date_from=date_from, date_to=date_to)
    data_count = dw.get_products_sale(by='qty', date_from=date_from, date_to=date_to)
    # Робиться один DataFrame з двох (кількість товару + оборот)
    table_plus_minus = data_count.append(data_oborot).T

    table_plus_minus.columns = [name_from_qtr, name_to_qtr, name_from_turnover,
                          name_to_turnover]  # Добавляються назви стовпців в табицю

    table_plus_minus = table_plus_minus[((table_plus_minus[name_from_qtr] - table_plus_minus[name_to_qtr]) != 0) & (
    (table_plus_minus[name_from_turnover] - table_plus_minus[name_to_turnover]) != 0) &
                            ((table_plus_minus[name_from_qtr] - table_plus_minus[name_to_qtr]) != 1 & (
                            (table_plus_minus[name_from_qtr] - table_plus_minus[name_to_qtr]) != -1))
                            ]
    table_plus_minus['Зміна кількості продаж'] = table_plus_minus[name_to_qtr] - table_plus_minus[name_from_qtr]
    table_plus_minus['Зміна обороту'] = table_plus_minus[name_to_turnover] - table_plus_minus[name_from_turnover]

    table_plus_minus.drop(table_plus_minus.columns[[0, 1, 2, 3]], axis=1, inplace=True)  # Видаляємо непотрібні стовці
    # list = [table_plus.head(30).T.columns.get_col(i) for i in table_plus.head(30).T.columns]
    ls = list(table_plus_minus.T.columns.values)  # Список назв товарів
    table_plus_minus.insert(0, u'Назва товару', ls)  # Добавляємо поле з списком назв товарів
    # Сортування табциці
    if plus_minus == 'plus':
        table = table_plus_minus.sort(columns=['Зміна кількості продаж', 'Зміна обороту'], ascending=[False, False])
    elif plus_minus == 'minus':
        table = table_plus_minus.sort(columns=['Зміна кількості продаж', 'Зміна обороту'],ascending=[True, True])
    return table



if __name__ == '__main__':
    pass
    #print main_table("2015-11-17", "2015-11-18")


