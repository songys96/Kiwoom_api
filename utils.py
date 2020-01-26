# -*- coding:utf-8 -*-

def change_money_format(data):
    striped = data.lstrip('-0')
    if striped == "":
        striped = '0'
    
    try:
        format_data = format(int(striped), ',d')
    except:
        format_data = format(float(striped))

    if data.startswith('-'):
        format_data = '-' + format_data

    return format_data

def change_percentage_format(data):
    strip_data = data.lstrip('-0')

    if strip_data == '':
        strip_data = '0'

    if strip_data.startswith('.'):
        strip_data = '0' + strip_data

    if data.startswith('-'):
        strip_data = '-' + strip_data

    return strip_data