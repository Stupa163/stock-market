import requests
from lxml import html
import time
from os.path import exists

URIS = [
    'dassault_systemes-stock',
    'ing-nl0011821202-stock'
]

DIR = 'data-files/'


def get_base_values(uris):
    max_values = {}

    for uri in uris:
        if exists(DIR + uri):
            file = open(DIR + uri, 'r')
            max_values[uri] = float(file.read())
        else:
            file = open(DIR + uri, 'w+')
            file.write('0')
            max_values[uri] = 0
        file.close()

    return max_values


def get_value(uri):
    content = requests.get('https://markets.businessinsider.com/stocks/' + uri)
    tree = html.fromstring(content.content)

    return float(tree.xpath('/html/body/main/div/div/div[3]/div/div[1]/div[1]/div[2]/div[1]/span')[0].text)


def new_max_value_to_file(uri, new_value):
    file = open(DIR + uri, 'w+')
    file.write(str(new_value))
    file.close()


def alert_low_value(uri, low_value):
    # Implements the desired alert there
    print('Alert ! Low value ! ' + low_value + ' for the ' + uri + ' stock')


maxs = get_base_values(URIS)

while True:
    for URI in URIS:
        value = get_value(URI)

        if value > maxs[URI]:
            maxs[URI] = value
            new_max_value_to_file(URI, value)
        elif value < maxs[URI] * (float(95) / 100):
            alert_low_value(URI, value)

        print(str(value) + ' => ' + str(maxs[URI]))
    time.sleep(2)
