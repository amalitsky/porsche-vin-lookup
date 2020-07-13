import requests
import sys
from bs4 import BeautifulSoup
from options import importantOptionCodesSet

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
    raise Exception('most likely VIN was not passed')

# seemingly useless noise
ignoredValues = [
    'Division',
    'Commission #',
    '\xa0',
]

ignoredValuesSet = set(ignoredValues)

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
