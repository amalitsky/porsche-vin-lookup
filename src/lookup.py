import requests
import sys
from bs4 import BeautifulSoup

if (len(sys.argv) != 2):
    raise Exception('most likely VIN is not passed')

vin = sys.argv[1]

host = 'vinanalytics.com'
url = '/car/' + vin + '/'

def getRowToPrint(value, label = '', isBold = False):
    str = ''

    if (isBold):
        str += '\033[1m'

    if (label):
        str += label + ': '

    str += value

    if (isBold):
        str += '\033[0m'

    return str

ignoredValues = [
    'Division',
    'Commission #',
    '\xa0',
]

ignoredValuesSet = set(ignoredValues)

goodCodes = [
    '9VL', # bose
    '9WT', # apple car play
    '030', # PASM 20mm
    '220', # PTV (prev gen GTS)
    '250', # PDK = no go
    '397', # 19" Boxster S Wheels
    '398', # 19" Cayman S Wheels
    '475', # Porsche Active Suspension Management (PASM) (Lowered 10 mm)
    '480', # manual
    '489', # heated multif steering
    '602', # LED headlights
    '603', # bi xenon
    '625', # entry & drive
    '680', # bose (prev gen)
    '858', # gt sport steering wheel
    '9VJ', # Burmester
    'A1', # black - no go
    'G1', # guards red
    'H2', # lava orange
    'J5', # maimi blue
    'P3', # racing yellow
    'P04', # Sport Seats Plus (2-way)
    'P07', # sport seat plus 18-way
    'QR5', # sport chrono
    'XEW', # Bi-Xenon Headlights in Black with Porsche Dynamic Light System
    'XLF', # sport exhaust 2016
    'XLX', # sport exhaust
]

goodCodesSet = sorted(set(goodCodes))

headerProperties = [
    'VIN',
    'BASE',
    'Prod Month',
    'Exterior',
    'Interior',
    'Price',
]

headerPropsSet = set(headerProperties)

request = requests.get('https://' + host + url)

soup = BeautifulSoup(request.text, features='html.parser')

table = soup.find('table')

if (table == None):
    raise Exception('most likely VIN was not found in DB')

tds = table('td')

tdsLength = len(tds)

valuesHash = {}

i = 0

propName = ''
propValue = ''

object = {}

while i < tdsLength:
    propName = tds[i].string.replace(':', '')
    propValue = tds[i+1].string

    if (propName not in ignoredValuesSet):
        object = {
            'name': propName,
            'value': propValue,
        }

        valuesHash[propName] = propValue

    i += 2

value = {}

key = ''

print('')

for propName in headerProperties:
    if (propName in valuesHash):
        print(
            getRowToPrint(
                value = valuesHash[propName],
                isBold = True,
            )
        )

print('')

keys = valuesHash.keys()

for key in goodCodesSet:
    if (key in valuesHash):
        print(
            getRowToPrint(
                value = valuesHash[key],
                label = key,
                isBold = True,
            )
        )

print('')

for key in keys:
    propValue = valuesHash[key]

    if (key in headerProperties or key in goodCodesSet):
        continue

    print(getRowToPrint(
        label = key,
        value = propValue,
        isBold = key in goodCodesSet,
    ))
