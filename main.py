# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 16:39:54 2019

@author: kevin
"""

import requests
import json
API_URL = 'http://api.poe.watch/'
LEAGUE = 'Blight'

def get(func, args):
    """Attempts to acces the poe.watch API with function string FUNC and arguments dictionary ARGS, returning the JSON value converted to python"""
    url = API_URL + func + '?' + ''.join([key+'='+args[key]+'&' for key in args])
    print('calling', url)
    result = requests.get(url)
    try:
        return json.loads(result.content)
    except:
        print(result, 'error')
        

def div_cards():
    return get('get', {'league':LEAGUE, 'category':'card'})