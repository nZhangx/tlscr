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
# 3 Modify `add_len` so that it returns the total length
    of all the numbers that appear as values in a JSON data structure.
"""