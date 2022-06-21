# A Tiny Little Web Scraper

This short lesson will show you how to build a fully functional web scraper.
We'll tackle the problem in three steps:
handling nested data,
handling HTML,
and finally getting HTML pages from the web.

## Nested Data

The list `flat` contains three strings:

```
flat = ["red", "green", "blue", "lime"]
```

If we want to get the total length of those strings,
we just add up the lengths of the items in `flat`:

```
total = 0
for word in flat:
    total += len(word)
```

If we have a list of lists,
we can use a double loop:

```
double = [["red", "green"], ["blue", "lime"]]
total = 0
for sublist in double:
    for word in sublist:
        total += len(word)
```

But what if we have a mix of words and lists?
What do we do if we have a structure like this:

```
irregular = ["red", ["green", "blue"], ["lime"]]
```

We could test the type of the item in the outer loop,
and only run the inner loop when the item is a sublist:

```
total = 0
for thing in irregular:
    if isinstance(thing, str):
        total += len(thing)
    elif isinstance(thing, list):
        for item in thing:
            total += len(item)
    else:
        print("Whoops, I don't know what", thing, "is")
```

That code isn't easy to read.
It also breaks as soon as we have sub-sub-lists like this:

```
nested = ["red", ["green", ["blue", "lime"]]]
```

To handle this,
we need to take a step back and write a function.
Here's our first attempt:

```
def add_len(thing):
    # If we're given a string, return its length immediately.
    if isinstance(thing, str):
        return len(thing)

    # If it's not a string, it had better be a list.
    assert isinstance(thing, list)

    # It's a list, so do something with each of its items.
    pass # What do we do here?
```

The last line of the code block above is the hard part.
We know we have a list.
We know it contains string and lists.
We want the total length of all the strings it contains.
If we had a magic function that could give us that total,
we'd be done:

```
def add_len(thing):
    if isinstance(thing, str):
        return len(thing)

    assert isinstance(thing, list)

    total = 0
    for item in thing: # we can loop because we know 'thing' is a list
        total += magic_function(item) # this is the part we're missing
    return total
```

But we *have* the magic function we need:
it's called `add_len`.
Let's plug that in to get the final version of `add_len`:

```
def add_len(thing):
    if isinstance(thing, str):
        return len(thing)

    assert isinstance(thing, list)

    total = 0
    for item in thing:
        total += add_len(item)
    return total
```

Let's trace its execution.

1.  `add_len("red")`:
    since `thing` is the string `"red"`,
    the function immediately returns 3.

2.  `add_len(["red"])`:
    `thing` is a list with one item,
    so we initialize `total` to 0 and go around our loop once.
    Inside the loop, we add `add_len("red")` to `total`.
    We've already established that `add_len("red")` returns 3,
    so we set `total` to 0+3,
    finish the loop,
    and return 3.

3.  `add_len(["red", "green"])`:
    OK, `thing` is a list with two items,
    so our loop calls `add_len("red")` and `add_len("green")`
    in that order,
    setting `total` to 3 and then 8
    and returns that.

4.  `add_len(["red", ["green", "blue"]])`:
    we'll trace this one point by point.
    The initial call to `add_len` sees a list so it goes to the bottom code.
    -   It initializes `total` to 0.
    -   The first time around the loop we call `add_len("red")`.
        This returns 3, so `total` becomes 3.
    -   The second time around the loop we call `add_len(["green", "blue"])`.
        Since we've given `add_len` a list,
        we go into a loop inside *that* call to the function.
        -   We initialize `total` to 0.
            This is *not* the same variable as the `total` mentioned above:
            this `total` belongs to the new call to `add_total`,
            just like different people each have their own nose.
        -   The first time around the loop we call `add_len("green")`.
            It returns 5, so we set this function call's `total` to 5.
        -   The second time around we call `add_len("blue")`,
            so total becomes 9.
        -   There's nothing else in the list, so this function call returns 9.
    -   We're now back in the initial function call.
        Its total is 3 (the length of `"red"`)
        and the call to `add_len(["green", "blue"])` just returned 9,
        so we set `total` to 12.
    -   There's nothing else in this function call's list,
        so we return 12
        and we're done.

This explanation is probably very confusing,
so please head over to <https://pythontutor.com/visualize.html#mode=edit>,
copy the `add_len` function into the text box,
add a line to call the function,
and then click on `[Visualize Execution]`.
As you click `[Next]`,
it will show you what's happening step by step as your code runs.

<div align="center">
  <img src="add_len.png" alt="Visualization of add_len function"/>
</div>

1.  Write a function called `join_all` that joins all the strings
    in a bunch of nested lists.
    For example:

    ```
    join_all([["red", ["green", "blue"]], "lime"])
    ```

    should return `"redgreenbluelime"`.

2.  Write a function called `longest` that returns the longest string it finds
    in a bunch of nested lists.
    For example:

    ```
    longest(["red", ["green", "blue"], ["lime"]])
    ```

    should return `"green"`.
    (If several strings are of equal longest length,
    return whichever you want.)

3.  JSON (short for "JavaScript Object Notation")
    consists of nested lists and dictionaries,
    where the dictionaries can only have strings as keys.
    For example,
    this is a valid JSON data structure:

    ```
    {"alpha": 1, "beta": {"gamma": [2, 3], "delta": [4, {"epsilon": 5}]}}
    ```

    It may be easier to read if it's written like this:

    ```
    {
        "alpha": 1,
        "beta": {
            "gamma": [
                2,
                3
            ],
            "delta": [
                4,
                {
                    "epsilon": 5
                }
            ]
        }
    }
    ```

    Modify `add_len` so that it returns the total length
    of all the numbers that appear as values in a JSON data structure.
    For example, the result for the data structure shown above is 15.

4.  Write a function `json_find` that takes a list of keys and indices
    and returns the part of a JSON structure at that location.
    For example, the list `["beta", "delta", 1]` should return the
    dictionary `{"epsilon":5}` in the structure above:
    -   The key `"beta"` selects a sub-dictionary.
    -   They key `"delta"` selects a list.
    -   The index 1 selects the second element of that list.
