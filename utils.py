import csv
import requests

LEAGUE = 'Blight'
div_cards = ''
all_data = ''
ITEM_DATA = ''
MEAN_NAME = ''


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


# API-specific functions

def _poe_watch_api(func, params):
    """Attempts to access the poe.watch API with function string FUNC and parameters dictionary PARAMS, returning the
    JSON value converted to python """
    api_url = 'http://api.poe.watch/'
    print('calling', func, params, 'to', api_url)
    result = requests.get(api_url + func, params=params)
    try:
        return result.json()
    except:
        print(result.status_code)


def _all_data_poe_watch():
    return _poe_watch_api('compact', {'league': LEAGUE})


def _div_cards_poe_watch():
    """Returns data all data on all div cards as a list of dictionaries"""
    return _poe_watch_api('get', {'league': LEAGUE, 'category': 'card'})


def set_api_poe_watch():
    """Sets the api from which to querry data to poe.watch"""
    global div_cards
    global all_data
    global ITEM_DATA
    global MEAN_NAME
    div_cards = _div_cards_poe_watch
    all_data = _all_data_poe_watch
    ITEM_DATA = all_data()
    MEAN_NAME = 'mean'


def _poe_ninja_api(func, params):
    """Attempts to access the poe.ninja API with function string FUNC and parameters dictionary PARAMS, returning the
    JSON value converted to a python list"""
    api_url = 'https://poe.ninja/api/Data/'
    print('calling', func, params, 'to', api_url)
    result = requests.get(api_url + func, params=params)
    try:
        return result.json()['lines']
    except:
        print(result.status_code)


def _all_data_poe_ninja():
    with open('poe_ninja_apis.csv', 'r', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        funcs = [item for sublist in reader for item in sublist]
    dics = []
    for func in funcs:
        dics.extend(_poe_ninja_api(func, {'league': LEAGUE}))
    dics.sort(key=lambda dic: dic['id'])
    return dics


def _div_cards_poe_ninja():
    return _poe_ninja_api('GetDivinationCardsOverview', {'league': LEAGUE})


def set_api_poe_ninja():
    """Sets the api from which to querry data to poe.ninja"""
    global div_cards
    global all_data
    global ITEM_DATA
    global MEAN_NAME
    div_cards = _div_cards_poe_ninja
    all_data = _all_data_poe_ninja
    ITEM_DATA = all_data()
    MEAN_NAME = 'chaosValue'


# Misc. functions


def lookup_price(target_id):
    """Uses binary search to look up the mean price of item ID"""

    def lookup_recursive(trgt_id, lower, upper):
        i = (lower + upper) // 2  # the midpoint of the two bounds
        current_id = ITEM_DATA[i]['id']  # id of the midpoint
        if lower > upper:
            raise ValueError('item id', id, 'not found')
        if current_id == trgt_id:
            return ITEM_DATA[i][MEAN_NAME]
        elif current_id < trgt_id:
            return lookup_recursive(trgt_id, i, upper)
        elif current_id > trgt_id:
            return lookup_recursive(trgt_id, lower, i)

    return lookup_recursive(target_id, 0, len(ITEM_DATA) - 1)


def trim_dics(dics):
    """Selects the name, stackSize, and mean entries of each entry of DICS"""

    def select(dic):
        return {entry: dic[entry] for entry in ['name', 'stackSize', MEAN_NAME]}

    return list(map(select, dics))


# Predicates

SELECTED_CARDS = open('div_cards.txt', 'r').read().splitlines()


def price_pred(dic, floor=40, ceil=2000):
    """Test if investment of item DIC is within range FLOOR and CEIL"""
    try:
        investment = dic[MEAN_NAME] * dic['stackSize']
        return floor <= investment <= ceil
    except KeyError:
        return False


def name_pred(dic):
    """Test if item name of DIC is in div_cards.txt"""
    try:
        return dic['name'] in SELECTED_CARDS
    except KeyError:
        return False
