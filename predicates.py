def price_pred(dic, floor, ceil):
    try:
        investment = dic['mean'] * dic['stackSize']
        return floor <= investment <= ceil
    except KeyError:
        return False
