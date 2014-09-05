#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# by Roman Vishnevsky aka.x0x01 @ gmail.com

import socket

# MAC адрес устройства. Заменить на свой!
DEVICE_MAC = 'b827ebdfa533'#b8:27:eb:df:a5:33

# идентификатор устройства, для простоты добавляется 01 (02) к mac устройства
SENSOR_ID_1 = DEVICE_MAC + '01'
SENSOR_ID_2 = DEVICE_MAC + '02'

# значения датчиков, тип float/integer
sensor_value_1 = 20
sensor_value_2 = -20.25

# создание сокета
sock = socket.socket()

# обработчик исключений
try:
    # подключаемся к сокету
    #sock.connect(('narodmon.ru', 8283))#62.252.172.241
    sock.connect(('62.252.172.241', 8283))

    # пишем в сокет еденичное значение датчика
    sock.send("#{}\n#{}#{}\n##".format(DEVICE_MAC, SENSOR_ID_1, sensor_value_1))

    # пишем в сокет множественные значение датчиков
    # sock.send("#{}\n#{}#{}\n#{}#{}\n##".format(DEVICE_MAC, SENSOR_ID_1, sensor_value_1, SENSOR_ID_2, sensor_value_2))

    # читаем ответ
    data = sock.recv(1024)
    sock.close()
    print data
except socket.error, e:
    print('ERROR! Exception {}'.format(e))
