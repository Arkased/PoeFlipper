import csv
import requests

API_URL = 'http://api.poe.watch/'
LEAGUE = 'Blight'


def load_id_dic():
    with open('item_ids.csv', 'r', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        id_dic = {row[0]: int(row[1]) for row in reader}
    return id_dic


ID_DIC = load_id_dic()


def save_dicts(dics: list):
    """Saves a list of dictionaries DICS as a csv file."""
    with open('out.csv', 'w', newline='') as f:
        wtr = csv.writer(f)
        wtr.writerow(dics[0].keys())
        for dic in dics:
            wtr.writerow(dic.values())


def api(func, params):
    """Attempts to access the poe.watch API with function string FUNC and parameters dictionary PARAMS, returning the
    JSON value converted to python """
    print('calling', func, params)
    result = requests.get(API_URL + func, params=params)
    try:
        return result.json()
    except:
        print(result.status_code)


def item_price(id):
    """Looks up the mean price of item ID"""
    return api('itemhistory', {'id': id, 'league': LEAGUE})['mean']


def div_cards():
    """Returns data all data on all div cards as a list of dictionaries"""
    return api('get', {'league': LEAGUE, 'category': 'card'})


def trim_dics(dics):
    """Selects the name, stackSize, and mean entries of each entry of DICS"""

    def select(dic):
        return {entry: dic[entry] for entry in ['name', 'stackSize', 'mean']}

    return list(map(select, dics))


# Predicates

SELECTED_CARDS = open('div_cards.txt', 'r').read().splitlines()


def price_pred(dic, floor=40, ceil=2000):
    """Test if investment of item DIC is within range FLOOR and CEIL"""
    try:
        investment = dic['mean'] * dic['stackSize']
        return floor <= investment <= ceil
    except KeyError:
        return False


def name_pred(dic):
    """Test if item name of DIC is in div_cards.txt"""
    try:
        return dic['name'] in SELECTED_CARDS
    except KeyError:
        return False
