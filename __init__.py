# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 16:39:54 2019

@author: kevin
"""

import utils

divs = utils.div_cards()
divs = filter(utils.price_pred, divs)
divs = filter(utils.name_pred, divs)
divs = utils.trim_dics(divs)

for div in divs:
    div['cost'] = div['mean'] * div['stackSize']
    div['returnId'] = utils.ID_DIC[div['name']]
    div['revenue'] = utils.lookup_price(div['returnId'])
    div['profit'] = (div['revenue'] - div['cost'])
    div['profitPerTrade'] = div['profit'] / (div['stackSize'] + 1)
    div['yield'] = 1 + div['profit'] / div['cost']

divs.sort(key=lambda d: -abs(d['profitPerTrade']) * d['yield'])
utils.save_dicts(divs)
