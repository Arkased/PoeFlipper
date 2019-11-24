import csv
import requests
import abc

SELECTED_CARDS = open('div_cards.txt', 'r').read().splitlines()


# noinspection PyBroadException
class APIAgent(abc.ABC):
    """
    Abstract agent for accessing APIs

    Attributes:
        APIAgent._mean_name: the name with which the api describes the average price (in chaos orbs) of an item
        APIAgent._api_url: the url through which to access the API
        APIAgent._id_file: the filename with names of div cards and item ids of their rewards
        APIAgent._id_dict: a dictionary containing the contents of id_file
        APIAgent._supported_cards: a list of cards which are supported
    """

    _mean_name = ''
    _api_url = ''
    _id_file = ''
    _id_dict: dict = {}
    _supported_cards = []

    def __init__(self, league: str):
        """Initializes an agent for league LEAGUE. The API is determined by the instantiating subclass."""
        # TODO: add selection option from active leagues (standard sc/hc and challenge sc/hc)
        self._league = league
        self._data = self._fetch_div_data()
        self._filter_name()
        self._item_data = self._fetch_all_data()
        self._trim_data()

    @classmethod
    def _set_id_dict(cls):
        cls._id_dict = cls._load_id_dict()

    @staticmethod
    def _load_id_dict(file_name):
        """Loads and returns a dictionary of the supported div cards and the item ids of their rewards"""
        # TODO: implement functionality to support rewards containing stacks of items
        with open(file_name, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=',')
            id_dic = {row[0]: int(row[1]) for row in reader}
        return id_dic

    def save_data(self):
        """Saves self.data as a csv file."""
        with open('out.csv', 'w', newline='') as f:
            wtr = csv.writer(f)
            wtr.writerow(self._data[0].keys())
            for dic in self._data:
                wtr.writerow(dic.values())

    @classmethod
    @abc.abstractmethod
    def _api(cls, func, params):
        """Accesses the API (dependent on the instantiating subclass) with function FUNC and parameters
        PARAMS, returning the JSON value."""

        print('calling', func, params, 'to', cls._api_url)
        result = requests.get(cls._api_url + func, params=params)
        try:
            return result.json()
        except:
            print(result.status_code)

    @abc.abstractmethod
    def _fetch_div_data(self):
        """Fetches data of all div cards from API (of instantiating subclass)."""
        pass

    @abc.abstractmethod
    def _fetch_all_data(self):
        """Fetches data on all items from API (of instantiating subclass)."""
        pass

    def _lookup_price(self, target_id):
        """Uses binary search to look up and return the current price of item with id TARGET_ID."""

        def lookup_recursive(trgt_id, lower, upper):
            i = (lower + upper) // 2  # the midpoint of the two bounds
            current_id = self._item_data[i]['id']  # id of the midpoint
            if lower > upper:
                print('item id', id, 'not found in', self._league)
                return 0
            if current_id == trgt_id:
                return self._item_data[i][self._mean_name]
            elif current_id < trgt_id:
                return lookup_recursive(trgt_id, i, upper)
            elif current_id > trgt_id:
                return lookup_recursive(trgt_id, lower, i)

        return lookup_recursive(target_id, 0, len(self._item_data) - 1)

    # Operations on APIAgent.data

    def _trim_data(self):
        """Selects the name, stackSize, and current price entries of each entry of self.data"""

        def select(dic):
            return {entry: dic[entry] for entry in ['name', 'stackSize', self._mean_name]}

        self._data = list(map(select, self._data))

    def _filter_name(self):
        """Filters div cards to only ones that are supported"""
        self._data = list(filter(lambda dic: dic['name'] in self._supported_cards, self._data))

    def filter_price(self, floor=40, ceil=2000):
        """Filters div cards with investment between FLOOR and CEIL"""
        self._data = list(filter(lambda dic: floor <= dic[self._mean_name] * dic['stackSize'] <= ceil, self._data))

    def calculate_profit(self):
        """Performs various calculations on self.data and sorts the results based on profit/trade and yield."""
        for div in self._data:
            div['investment'] = div[self._mean_name] * div['stackSize']
            div['returnId'] = self._id_dict[div['name']]
            div['return'] = self._lookup_price(div['returnId'])
            div['profit'] = (div['return'] - div['investment'])
            div['profitPerTrade'] = div['profit'] / (div['stackSize'] + 1)
            div['yield'] = 1 + div['profit'] / div['investment']
        self._data.sort(key=lambda d: d['profitPerTrade'] * d['yield'], reverse=True)


class WatchAPIAgent(APIAgent):
    _mean_name = 'mean'
    _api_url = 'http://api.poe.watch/'
    _id_file = 'watch_item_ids.csv'
    _id_dict: dict = APIAgent._load_id_dict(_id_file)
    _supported_cards = _id_dict.keys()

    @classmethod
    def _api(cls, func, params):
        return super()._api(func, params)

    def _fetch_all_data(self):
        return self._api('compact', {'league': self._league})

    def _fetch_div_data(self):
        return self._api('get', {'league': self._league, 'category': 'card'})

# class NinjaAPIAgent(APIAgent):
#     _mean_name = 'chaosValue'
#     api_url = 'https://poe.ninja/api/Data/'
#     # TODO: create file
#     id_file = 'ninja_item_ids.csv'
#     _id_dict: dict = APIAgent._load_id_dict(id_file)
#     supported_cards = _id_dict.keys()
#
#     @classmethod
#     def _api(cls, func, params):
#         return super()._api(func, params)['lines']
#
#     def _fetch_all_data(self):
#         # TODO: Implement support for currencies and fragments (different format)
#         # TODO: Update APIs
#         with open('ninja_apis.csv', 'r', newline='') as f:
#             reader = csv.reader(f, delimiter=',')
#             funcs = [item for sublist in reader for item in sublist]
#         all_data = []
#         for func in funcs:
#             all_data.extend(self._api(func, {'league': self._league}))
#         all_data.sort(key=lambda dic: dic['id'])
#         return all_data
#
#     def _fetch_div_data(self):
#         return self._api('GetDivinationCardsOverview', {'league': self._league})
