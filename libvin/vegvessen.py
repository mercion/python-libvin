"""
Fetch a VIN record from Vegvessen.no this is the national vehicle
registry in Norway.

(c) Copyright 2018 Mercion Wilathgamuwage  <mercion@evlynk.com>
License: AGPL v3.0
"""

import requests
import logging
from lxml import etree

log = logging.getLogger('libvin.vegvessen')

interesting_keys = {
    'merke': 'manufacturer',
    'modell': 'model',
    'type': 'type',
    'brukstype/gruppe': 'class',
    'farge': 'color',
    'seter': 'seats',
    'drivstofftype': 'fuel type',
    'motorytelse/oppgitt': 'motor power',
    'motorytelse/oppgittBenevning': 'motor power units',
    'hestekrefter': 'horse power',
    'maxhastighet': 'max speed',
    'egenvektMedForer': 'weight with driver',
    'regnr': 'registration number',
    'forstegangsreg': 'date of first registration',
    'registrertDistrikt': 'registration location',
    'egenvekt': 'weight',
    'lengde': 'length',
    'bredde': 'bredth',
    'dekkdimensjonForan': 'front wheel size',
    'understellsnr': 'vin',
    'dekkdimensjonBak': 'rear wheel size'}

def _get_xpath_text(node, name):
    matches = node.xpath(name)
    if matches:
        return matches[0].text.strip()

def vegvessen_decode(vin):
    '''
    Return vegvessen.no's informtion about this VIN
    '''
    url = 'https://www.vegvesen.no//System/mobilapi?registreringsnummer=' + vin
    try:
        r = requests.get(url)
    except requests.Timeout:
        log.error('vegvessen.no connection timedout')
        return None
    except requests.ConnectionError:
        log.error('vegvessen.no connection failed')
        return None
    except:
        log.error('Unexpected error when connectiong to vegvessen.no')
        return None

    if r.ok:
        raw_xml = r.content
        root = etree.fromstring(raw_xml)
        result = {}
        for xpath, key in interesting_keys.items():
            result[key] = _get_xpath_text(root, xpath)
        return result
    return {}

