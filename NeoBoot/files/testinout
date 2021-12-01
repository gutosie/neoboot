#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from os import system
import time
from Tools.Directories import fileExists, SCOPE_PLUGINS


def getAccesDate():
    timego = ''
    dana = getTestOutTime()   #  etc   Nie! Szukana liczba jest wieksza!
    strzal = getTestInTime()  #  tmp   Nie! Szukana liczba jest mniejsza!
    if strzal == dana:
        timego = 'access'
    elif strzal < dana:
        timego = 'isaccess'
    else:
        timego = 'timeoff'
        os.system('echo "19700101"  > /usr/lib/periodon/.kodn')
    return timego


def getTestCzas():
    mytestnC = ''
    if os.path.exists('/usr/lib/periodon/.accessdate'):
        with open('/usr/lib/periodon/.accessdate', 'r') as f:
            mytestnC = f.readline().strip()
            f.close()
    return mytestnC


def getTestToTest():
    mytestnb = ''
    if os.path.exists('/tmp/.nkod'):
        with open('/tmp/.nkod', 'r') as f:
            mytestnb = f.readline().strip()
            f.close()
    return mytestnb


def getTestIn():
    neopluspro = 'UNKNOWN'
    if os.path.exists('/usr/lib/periodon/.kodn'):
        with open('/usr/lib/periodon/.kodn', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('1234' + getTestToTest() + '') != -1:
            neopluspro = '1234%s' % getTestToTest()
    return neopluspro


def getTestOut():
    neoplus = 'UNKNOWN'
    if os.path.exists('/tmp/.nkod'):
        with open('/tmp/.nkod', 'r') as f:
            lines2 = f.read()
            f.close()
        if lines2.find("%s" % getTestToTest()) != -1:
            neoplus = '1234%s' % getTestToTest()
    return neoplus


def getAccessN():
    neopro = ''
    if os.path.exists('/usr/lib/periodon/.kodn'):
        with open('/usr/lib/periodon/.kodn', 'r') as f:
            neopro = f.readline().strip()
            f.close()
    return neopro


def getTestInTime():
    mydatein = 'UNKNOWN'
    if os.path.exists('/tmp/.finishdate'):
        with open('/tmp/.finishdate', 'r') as f:
            mydatein = f.readline().strip()
            f.close()
    return mydatein


def getTestOutTime():
    mydateout = 'UNKNOWN'
    if os.path.exists('/usr/lib/periodon/.accessdate'):
        with open('/usr/lib/periodon/.accessdate', 'r') as f:
            mydateout = f.readline().strip()
            f.close()
    return mydateout


def getButtonPin():
    mypin = 'UNKNOWN'
    if os.path.exists('/usr/lib/periodon'):
        out = open('/usr/lib/periodon/.kodn', 'w')
        out.write('1234%s' % getTestToTest())
        out.close()
        mypin = 'pinok'
    return mypin
