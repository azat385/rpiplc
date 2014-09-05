#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# by Roman Vishnevsky aka.x0x01 @ gmail.com

import urllib2
import urllib

# MAC адрес устройства. Заменить на свой!
DEVICE_MAC = '0123456789012'

# идентификатор устройства, для простоты добавляется 01 (02) к mac устройства
SENSOR_ID_1 = DEVICE_MAC + '01'
SENSOR_ID_2 = DEVICE_MAC + '02'

# значения датчиков, тип float/integer
sensor_value_1 = 28
sensor_value_2 = -12.34

# формирование POST запроса для единичного датчика
data = urllib.urlencode({
    'ID': DEVICE_MAC,
    SENSOR_ID_1: sensor_value_1
})

# формирование POST запроса для 2х датчиков
# data = urllib.urlencode({
#     'ID': DEVICE_MAC,
#     SENSOR_ID_1: sensor_value_1,
#     SENSOR_ID_2: sensor_value_2
# })


# формирование заголовков запроса
headers = {
    'Content-Length': str(len(data)),
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'narodmon.ru'
}

# непосредственно запрос
request = urllib2.Request('http://narodmon.ru/post.php', data, headers)
response = urllib2.urlopen(request)
print response.headers
