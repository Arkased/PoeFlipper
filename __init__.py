# -*- coding: utf-8 -*-
"""
Created on Wed Oct 2 16:39:54 2019

@author: Kevin Liu
"""

import APIAgent

league = 'Blight'

agent = APIAgent.WatchAPIAgent(league)
# agent = APIAgent.NinjaAPIAgent(league)
# agent.filter_price()

agent.calculate_profit()
agent.save_data()
