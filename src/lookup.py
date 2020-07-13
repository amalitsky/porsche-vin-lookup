import requests
import sys
from bs4 import BeautifulSoup

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

if (len(sys.argv) != 2):
    raise Exception('most likely VIN is not passed')

# seemingly useless noise
ignoredValues = [
    'Division',
    'Commission #',
    '\xa0',
]

ignoredValuesSet = set(ignoredValues)

importantOptionCodes = [
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

importantOptionCodesSet = sorted(set(importantOptionCodes))

# top report section
headerProps = [
    'VIN',
    'BASE',
    'Prod Month',
    'Exterior',
    'Interior',
    'Price',
]

headerPropsSet = set(headerProps)

vin = sys.argv[1]
host = 'vinanalytics.com'
path = '/car/' + vin + '/'

request = requests.get('https://' + host + path)

soup = BeautifulSoup(request.text, features='html.parser')
table = soup.find('table')

if (table == None):
    raise Exception('most likely VIN was not found on ' + host)

tds = table('td')
tdsLength = len(tds)

valuesHash = {}

i = 0
key = ''
propValue = ''

while i < tdsLength:
    key = tds[i].string.replace(':', '')
    propValue = tds[i+1].string

    if (key not in ignoredValuesSet):
        valuesHash[key] = propValue

    i += 2

# empty line
print('')

for key in headerPropsSet:
    if (key in valuesHash):
        print(
            getRowToPrint(
                value = valuesHash[key],
                isBold = True,
            )
        )

print('')

# "important" options
for key in importantOptionCodesSet:
    if (key in valuesHash):
        print(
            getRowToPrint(
                value = valuesHash[key],
                label = key,
                isBold = True,
            )
        )

print('')

keys = sorted(valuesHash.keys())

# rest of options
for key in keys:
    propValue = valuesHash[key]

    if (key in headerPropsSet or key in importantOptionCodesSet):
        continue

    print(
        getRowToPrint(
            label = key,
            value = propValue,
            isBold = key in importantOptionCodesSet,
        )
    )
