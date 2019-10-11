import csv
import requests

API_URL = 'http://api.poe.watch/'
LEAGUE = 'Blight'


def api(func, params):
    """Attempts to access the poe.watch API with function string FUNC and parameters dictionary PARAMS, returning the
    JSON value converted to python """
    print('calling', params)
    result = requests.get(API_URL + func, params=params)
    try:
        return result.json()
    except:
        print(result.status_code)


def save_dicts(dics: list):
    """Saves a list of dictionaries DICS as a csv file."""
    with open('out.csv', 'w', newline='') as f:
        wtr = csv.writer(f)
        wtr.writerow(dics[0].keys())
        for dic in dics:
            wtr.writerow(dic.values())


def div_cards():
    """Returns data all data on all div cards as a list of dictionaries"""
    return api('get', {'league': LEAGUE, 'category': 'card'})


def filtered_div(pred):
    """Filters the div cards returned by div_cards() with some predicate PRED, and additionally selects the name,
    stackSize, and mean columns."""

    def select(dic):
        return {entry: dic[entry] for entry in ['name', 'stackSize', 'mean']}

    div = div_cards()
    return list(map(select, filter(pred, div)))


# Predicates


SELECTED_CARDS = open('div_cards.txt', 'r').read().splitlines()


def price_pred(dic, floor, ceil):
    try:
        investment = dic['mean'] * dic['stackSize']
        return floor <= investment <= ceil
    except KeyError:
        return False


def name_pred(dic):
    try:
        return dic['name'] in SELECTED_CARDS
    except KeyError:
        return False
