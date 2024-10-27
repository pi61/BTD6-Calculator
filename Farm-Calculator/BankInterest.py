BANK_CAPACITY = 9500
TOP_CROSSPATH = 2

def get_income_per_round():
    return get_income_per_tick() * get_tickrate()

def get_tickrate():
    if TOP_CROSSPATH == 1:
        return 6
    elif TOP_CROSSPATH == 2:
        return 8
    else:
        return 4

def get_income_per_tick():
    if TOP_CROSSPATH == 1:
        return 286/3
    elif TOP_CROSSPATH == 2:
        return 338/8
    else:
        return 234/4
    
def get_interest(cash):
    return (cash * 115/100)
    
def next_round(cash): 
    return min(BANK_CAPACITY, get_interest(cash + get_income_per_round()))
    
def get_rounds_until_full(missed_ticks):
        cash = get_interest(get_income_per_round() - missed_ticks * get_income_per_tick())
        result = [round(cash,2)]
        while cash < BANK_CAPACITY:
            cash = next_round(cash)
            result.append(round(cash,2))
        return result

print(get_rounds_until_full(0))
