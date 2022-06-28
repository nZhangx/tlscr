def add_len(thing):
    if isinstance(thing, str):
        return len(thing)

    assert isinstance(thing, list)

    total = 0
    for item in thing:
        total += add_len(item)
    return total


print(add_len(["red", ["green", "blue"]]))

"""
#1 Write a function called `join_all` that joins all the strings
    in a bunch of nested lists.
"""

def join_all(thing):
    if isinstance(thing, str):
        return thing 

    assert isinstance(thing, list)

    total = ""
    for item in thing:
        total += join_all(item)
    return total 

print(join_all([["red", ["green", "blue"]], "lime"]))

"""
#2 Write a function called `longest` that returns the longest string it finds
    in a bunch of nested lists.
"""

def longest(thing, longests=""):
    if isinstance(thing, str):
        longests = thing if len(thing)>len(longests) else longests
        return longests

    assert isinstance(thing, list)

    for item in thing:
        if isinstance(item,str) and len(item)>len(longests):
            longests = item
        else:
            longests = longest(item,longests)
    return longests  

print(longest(["red", ["green", "blue"], ["lime"]]))

"""
# 3 Modify `add_len` so that it returns the total sum
    of all the numbers that appear as values in a JSON data structure.
"""

def add_len_sum(thing):
    if isinstance(thing, int):
        return thing
    elif isinstance(thing,list):
        sum_all = 0
        for item in thing:
            sum_all += add_len_sum(item)
        return sum_all
        
    assert isinstance(thing, dict)

    total = 0
    for __, item in thing.items():
        total += add_len_sum(item)
    return total

import json
with open("test_len_sum.json",'r') as f:
    js = json.load(f)
    print(add_len_sum(js))

"""
#4 Write a function `json_find` that takes a list of keys and indices
    and returns the part of a JSON structure at that location.
    For example, the list `["beta", "delta", 1]` should return the
    dictionary `{"epsilon":5}` in the structure above:
    -   The key `"beta"` selects a sub-dictionary.
    -   They key `"delta"` selects a list.
    -   The index 1 selects the second element of that list.
"""

def json_find(keys, curdict={}):
    if not isinstance(keys,list):
        assert keys in curdict
        return curdict[keys]
    else:
        return json_find(keys[1:],curdict[keys[0]])

