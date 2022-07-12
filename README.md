# A Tiny Little Web Scraper

This short lesson will show you how to build a fully functional web scraper.
We'll tackle the problem in three steps:
handling nested data,
handling HTML,
and finally getting HTML pages from the web.

### Env:
`conda activate scraper`


## Nested Data

The list `flat` contains three strings:

```python
flat = ["red", "green", "blue", "lime"]
```

If we want to get the total length of those strings,
we just add up the lengths of the items in `flat`:

```python
total = 0
for word in flat:
    total += len(word)
```

If we have a list of lists,
we can use a double loop:

```python
double = [["red", "green"], ["blue", "lime"]]
total = 0
for sublist in double:
    for word in sublist:
        total += len(word)
```

But what if we have a mix of words and lists?
What do we do if we have a structure like this:

```python
irregular = ["red", ["green", "blue"], ["lime"]]
```

We could test the type of the item in the outer loop,
and only run the inner loop when the item is a sublist:

```python
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

```python
nested = ["red", ["green", ["blue", "lime"]]]
```

To handle this,
we need to take a step back and write a function.
Here's our first attempt:

```python
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

```python
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

```python
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
  <img src="img/add_len.png" alt="Visualization of add_len function"/>
</div>

### Exercises

1.  Write a function called `join_all` that joins all the strings
    in a bunch of nested lists.
    For example:

    ```python
    join_all([["red", ["green", "blue"]], "lime"])
    ```

    should return `"redgreenbluelime"`.

2.  Write a function called `longest` that returns the longest string it finds
    in a bunch of nested lists.
    For example:

    ```python
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

    ```python
    {"alpha": 1, "beta": {"gamma": [2, 3], "delta": [4, {"epsilon": 5}]}}
    ```

    It may be easier to read if it's written like this:

    ```python
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

    Modify `add_len` so that it returns the sum 
    of all the numbers that appear as values in a JSON data structure.
    For example, the result for the data structure shown above is 15.

4.  Write a function `json_find` that takes a list of keys and indices
    and returns the part of a JSON structure at that location.
    For example, the list `["beta", "delta", 1]` should return the
    dictionary `{"epsilon":5}` in the structure above:
    -   The key `"beta"` selects a sub-dictionary.
    -   They key `"delta"` selects a list.
    -   The index 1 selects the second element of that list.

## A Quick Introduction to HTML and CSS

HTML is the standard way to represent documents for presentation in web browsers,
and CSS is the standard way to describe how it should look.
Both are more complicated than they should have been,
but in order to scrape data we need to understand a little of both.

An HTML document contains elements, text, and possibly other things that we will ignore for now.
Elements are shown using tags:
an opening tag `<tagname>` shows where the element begins,
and a corresponding closing tag `</tagname>` (with a leading slash) shows where it ends.
If there's nothing between the two, we can write `<tagname/>` (with a trailing slash).

A document's elements must form a tree,
i.e.,
they must be strictly nested.
This means that if Y starts inside X,
Y must end before X ends,
so `<X>…<Y>…</Y></X>` is legal,
but `<X>…<Y>…</X></Y>` is not.
Finally,
every document should have a single root element that encloses everything else,
although browsers aren't strict about enforcing this.
(In fact,
most browsers are pretty relaxed about enforcing any kind of rules…)

The text in an HTML page is normal printable text.
However,
since `<` and `>` are used to show where tags start and end,
we must use escape sequences to represent them,
just like we use `\"` to represented a literal double-quote character
inside a double-quoted string in Python.
In HTML,
escape sequences are written `&name;`,
i.e.,
an ampersand, the name of the character, and a semi-colon.
A few common escape sequences are shown below:

| Name         | Escape Sequence | Character |
| ------------ | --------------- | --------- |
| Less than    | `&lt;`          | <         |
| Greater than | `&gt;`          | >         |
| Ampersand    | `&amp;`         | &         |
| Copyright    | `&copy;`        | ©         |
| Plus/minus   | `&plusmn;`      | ±         |
| Micro        | `&micro;`       | µ         |

The first two are self-explanatory,
and `&amp;` is needed so that we can write a literal ampersand.
`&copy;`, `&plusmn;`, and `&micro;` are usually not needed any longer,
since most editors will allow us to put non-ASCII characters directly into documents these days,
but occasionally we will run into older or stricter systems.

A well-formed HTML page has:

-   a single `html` element that encloses everything else,
-   a single `head` element that contains information about the page, and
-   a single `body` element that contains the content to be displayed.

It doesn't matter whether or how we indent the tags showing these elements and the content they contain,
but laying them out on separate lines
and indenting to show nesting
helps human readers.
Well-written pages also use comments, just like code:
these start with `<!--` and end with `-->`.
Unfortunately,
comments cannot be nested,
i.e.,
if you comment out a section of a page that already contains a comment,
the results are unpredictable.

Here's an empty HTML page with the structure described above:

```html
<html>
  <head>
    <!-- description of page goes here -->
  </head>
  <body>
    <!-- content of page goes here -->
  </body>
</html>
```

Nothing shows up if we open this in a browser,
so let's add a little content:

```html
<html>
  <head>
    <title>Page Title (shown in browser bar)</title>
  </head>
  <body>
    <h1>Displayed Content Starts Here</h1>
    <p>
      This <em>lesson</em> shows
      how to scrape <strong>web pages</strong>.
    </p>
  </body>
</html>
```

-   The `title` element inside `head` gives the page a title.
    This is displayed in the browser bar when the page is open,
    but is *not* displayed as part of the page itself.

-   The `h1` element is a level-1 heading;
    we can use `h2`, `h3`, and so on to create sub-headings.

-   The `p` element is a paragraph.

-   Inside a heading or a paragraph,
    we can use `em` to *emphasize* text.
    We can also use `strong` to make text **stronger**.
    Tags like these are better than tags like `i` (for italics) or `b` (for bold)
    because they signal intention rather than forcing a particular layout.
    Someone who is visually impaired, or someone using a small-screen device,
    may want emphasis of various kinds displayed in different ways.

Elements can be customized by giving them attributes,
which are written as `name="value"` pairs inside the element's opening tag.
For example:

```html
<h1 align="center">A Centered Heading</h1>
```

centers the `h1` heading on the page, while:

```html
<p class="disclaimer">This planet provided as-is.</p>
```

marks this paragraph as a disclaimer.
That doesn't mean anything special to HTML,
but as we'll see later,
we can define styles based on the `class` attributes of elements.

An attribute's name may appear at most once in any element,
just like a key can only appear once in a Python dictionary,
so `<p align="left" align="right">…</p>` is illegal
(though again, most browsers won't complain).
If we want to give an attribute multiple values---for example,
if we want an element to have several classes---we put all the values in one string.
Unfortunately,
as the example below shows,
HTML is inconsistent about whether values should be separated by spaces or semi-colons:

```html
<p class="disclaimer optional" style="color: blue; font-size: 200%;">
```

However they are separated,
values are supposed to be quoted,
but in practice we can often get away with `name=value`.
And for Boolean attributes whose values are just true or false,
we can even sometimes just get away with `name` on its own.

Headings and paragraphs are all very well,
but data scientists need more.
To create an unordered (bulleted) list,
we use a `ul` element,
and wrap each item inside the list in `li`.
To create an ordered (numbered) list,
we use `ol` instead of `ul`,
but still use `li` for the list items.

```html
<ul>
  <li>first</li>
  <li>second</li>
  <li>third</li>
</ul>
```

produces:

> - first
> - second
> - third

while:

```html
<ol>
  <li>first</li>
  <li>second</li>
  <li>third</li>
</ol>
```

produces:

> 1. first
> 1. second
> 1. third

Lists can be nested by putting the inner list's `ul` or `ol`
inside one of the outer list's `li` elements.

Unsurprisingly,
we use the `table` element to create tables.
Each row is a `tr` (for ``table row''),
and within rows,
column items are shown with `td` (for ``table data'')
or `th` (for ``table heading''),
so:

```html
<table>
  <tr> <th>Alkali</th>   <th>Noble Gas</th> </tr>
  <tr> <td>Hydrogen</td> <td>Helium</td>    </tr>
  <tr> <td>Lithium</td>  <td>Neon</td>      </tr>
  <tr> <td>Sodium</td>   <td>Argon</td>     </tr>
</table>
```

produces:

> <table>
>   <tr> <th>Alkali</th>   <th>Noble Gas</th> </tr>
>   <tr> <td>Hydrogen</td> <td>Helium</td>    </tr>
>   <tr> <td>Lithium</td>  <td>Neon</td>      </tr>
>   <tr> <td>Sodium</td>   <td>Argon</td>     </tr>
> </table>

What we *should* write is:

```html
<table>
  <thead>
    <tr> <th>Alkali</th>   <th>Noble Gas</th> </tr>
  </thead>
  <tbody>
    <tr> <td>Hydrogen</td> <td>Helium</td>    </tr>
    <tr> <td>Lithium</td>  <td>Neon</td>      </tr>
    <tr> <td>Sodium</td>   <td>Argon</td>     </tr>
  </tbody>
</table>
```

Links to other pages are what make HTML hypertext.
Confusingly,
the element used to show a link is called `a`.
The text inside the element is displayed and (usually) highlighted for clicking.
Its `href` attribute specifies what the link is pointing at;
both local filenames and URLs are supported.
Oh,
and we can use `<br/>` to force a line break in text
(with a trailing slash inside the tag, since the `br` element doesn't contain any content):

```html
<a href="https://deepgenomics.com">Deep Genomics</a>
<br/>
<a href="https://third-bit.com/">Greg Wilson</a>
<br/>
<a href="img/add_len.png">Relative path</a>
```

produces:

> <a href="https://deepgenomics.com">Deep Genomics</a>
> <br/>
> <a href="https://third-bit.com/">Greg Wilson</a>
> <br/>
> <a href="img/add_len.png">Relative path</a>

Images can be stored directly inside HTML pages in a couple of different ways,
but it's far more common to store each image in a separate file
and refer to that file using an `img` element
(which also allows us to use the image in many places without copying it).
The `src` attribute of the `img` tag specifies where to find the file;
as with the `href` attribute of an `a` element,
this can be either a URL or a local path.
Every `img` should also include a `title` attribute (whose purpose is self-explanatory)
and an `alt` attribute with some descriptive text to aid accessibility and search engines.

```html
<img src="./img/logo.png" title="Book Logo"
     alt="Displays the book logo using a local path" />
<img src="https://third-bit.com/sd4ds/img/logo.png"
     title="Book Logo"
     alt="Display the book logo using a URL" />
```

Two things to note here are:

1.  Since `img` elements don't contain any text,
    they are often written with the trailing-slash notation,
    or as `<img src="...">` without any slashes at all.

2.  If an image file is referred to using a path rather than a URL,
    that path can be either relative
    or absolute.
    If it's a relative path,
    it's interpreted starting from where the web page is located;
    if it's an absolute path,
    it's interpreted relative to wherever the web browser has been told
    the root directory of the filesystem is.

When HTML first appeared, people styled elements by setting their attributes:

```html
<html>
  <body>
    <h1 align="center">Heading is Centered</h1>
    <p>
      <b>Text</b> can be highlighted
      or <font color="coral">colorized</font>.
    </p>
  </body>
</html>
```

Many still do,
but a better way is to use Cascading Style Sheets (CSS).
These allow us to define a style once and use it many times,
which makes it much easier to maintain consistency.
Here's a page that uses CSS instead of direct styling:

```html
<html>
  <head>
    <link rel="stylesheet" href="simple-style.css" />
  </head>
  <body>
    <h1 class="title">Heading is Centered</h1>
    <p>
      <span class="keyword">Text</span> can be highlighted
      or <span class="highlight">colorized</span>.
    </p>
  </body>
</html>
```

The `head` contains a link to an external style sheet
stored in the same directory as the page itself;
we could use a URL here instead of a relative path,
but the `link` element *must* have the `rel="stylesheet"` attribute.
Inside the page,
we then set the `class` attribute of each element we want to style.

The file `simple-style.css` looks like this:

```css
h1.title {
  text-align: center;
}
span.keyword {
  font-weight: bold;
}
.highlight {
  color: coral;
}
```

Each entry has the form `tag.class` followed by a group of properties inside curly braces,
and each property is a key-value pair.
We can omit the class and just write (for example):

```css
p {
  font-style: italic;
}
```

in which case the style applies to everything with that tag.
If we do this,
we can override general rules with specific ones:
the style for a disclaimer paragraph is defined by `p` with overrides defined by `p.disclaimer`.
We can also omit the tag and simply use `.class`,
in which case every element with that class has that style.

CSS can also match specific elements:
we can label particular elements uniquely within a page using the `id` attribute,
then refer to those elements using `#name` as a selector.
For example,
if we create a page that gives two spans unique IDs:

```html
<html>
  <head>
    <link rel="stylesheet" href="selector-style.css" />
  </head>
  <body>
    <p>
      First <span id="major">keyword</span>.
    </p>
    <p>
      Full <span id="minor">explanation</span>.
    </p>
  </body>
</html>
```

then we can style those spans like this:

```css
span#major {
  text-decoration: underline red;
}
span#minor {
  text-decoration: overline blue;
}
```

<div class="callout" markdown="1">
### Internal Links

We can link to an element in a page using `#name`
inside the link's `href`:
for example,
`<a href="page.html#place">text</a>`
refers to the `#place` element in `page.html`.
This is particularly useful *within* pages:
`<a href="#place">jump</a>`
takes us straight to the `#place` element within this page.
Internal links like this are often used for cross-referencing and to create a table of contents.
</div>

## Processing HTML

Python's standard library includes an HTML parser called `html.parser`,
but since the HTML found in the wild often doesn't comply with standards,
most people use a more resilient library called [Beautiful Soup][bs] to read pages instead.
You can install it with `pip install bs4` or `conda install bs4`.
To show how it works,
here's a short HTML page called `species.html`:

```html
<html>
  <head>
    <title>Species Information</title>
  </head>
  <body>
    <h1>Species Information</h1>
    <p>
      All information from
      <a href="https://en.wikipedia.org/wiki/List_of_birds_of_Ontario">Wikipedia</a>.
    </p>
    <ul>
      <li>Snow goose <em>Anser caerulescens</em></li>
      <li>Mute swan <em>Cygnus olor</em></li>
      <li>Green-winged teal <em>Anas crecca</em></li>
      <li>Smew <em>Mergellus albellus</em></li>
      <li>Histrionic duck <em>Histrionicus histrionicus</em></li>
    </ul>
  </body>
</html>
```

Let's load that page with Beautiful Soup:

```python
from bs4 import BeautifulSoup, Tag, NavigableString

def show(node, depth):
    if isinstance(node, Tag):
        print("  " * depth, node.name, "+", node.attrs)
        for child in node.contents:
            show(child, depth + 1)
    elif isinstance(node, NavigableString):
        print("  " * depth, "==", repr(node.string))
    else:
        print("  " * depth, f"I don't know what {node} is")

with open("species.html", "r") as reader:
    doc = BeautifulSoup(reader, "html.parser")
    show(doc, 0)
```

This program's output is:

```text
 [document] + {}
   html + {}
     == '\n'
     head + {}
       == '\n'
       title + {}
         == 'Species Information'
       == '\n'
     == '\n'
     body + {}
       == '\n'
       h1 + {}
         == 'Species Information'
       == '\n'
       p + {}
         == '\n      All information from\n      '
         a + {'href': 'https://en.wikipedia.org/wiki/List_of_birds_of_Ontario'}
           == 'Wikipedia'
         == '.\n    '
       == '\n'
       ul + {}
         == '\n'
         li + {'class': ['species']}
           == 'Snow goose '
           em + {}
             == 'Anser caerulescens'
         == '\n'
         li + {'class': ['species']}
           == 'Mute swan '
           em + {}
             == 'Cygnus olor'
         == '\n'
         li + {'class': ['species']}
           == 'Green-winged teal '
           em + {}
             == 'Anas crecca'
         == '\n'
         li + {'class': ['species']}
           == 'Smew '
           em + {}
             == 'Mergellus albellus'
         == '\n'
         li + {'class': ['species']}
           == 'Histrionic duck '
           em + {}
             == 'Histrionicus histrionicus'
         == '\n'
       == '\n'
     == '\n'
   == '\n'
```

What it shows is that:

-  Beautiful Soup creates a single `document` node to contain the whole document.
-  That node has a single child with the tag `html`,
   which has a `head` and a `body` node as its children.
   In between those children are some text elements holding
   the spaces and newlines we used for indentation in our document.
-  We can get the tag of a node using `node.name`
   and a dictionary of its attributes using `node.attrs`.

We could find things in this tree by writing a `search` function
that recursed down through the nodes the same way that `show` does,
but this is such a common operation that Beautiful Soup provides a bunch of search functions for us:

```python
from bs4 import BeautifulSoup

with open("species.html", "r") as reader:
    doc = BeautifulSoup(reader, "html.parser")
    heading = doc.find("h1")
    print(heading.string)
```
```text
Species Information
```

Notice that the `.string` property of a node returns the text inside that node.

Here's a more interesting search:

```python
from bs4 import BeautifulSoup

with open("species.html", "r") as reader:
    doc = BeautifulSoup(reader, "html.parser")
    species = doc.find_all("li", attrs={"class": "species"})
    print("Common,Scientific")
    for node in species:
        # first child is a string
        common = node.contents[0].strip()
        # scientific name in 'em'
        scientific = node.find("em").string.strip()
        print(f"{common},{scientific}")
```
```text
Common,Scientific
Snow goose,Anser caerulescens
Mute swan,Cygnus olor
Green-winged teal,Anas crecca
Smew,Mergellus albellus
Histrionic duck,Histrionicus histrionicus
```

The three most important things about this example are:

1.  We don't have to search the document ourselves:
    Beautiful Soup will find what we need.

1.  But we *do* have to know how to specify what we're looking for…

1.  …and the document has to be regularly structured.
    If the species' names were scattered throughout paragraphs of plain text,
    finding them would be a lot more work.

### Exercises (for the week of June 28-July 5)

1.  Write a program to count the number of tables in `table.html`.

1.  Write a program that combines all the information from tables with the class `species`
    into a single CSV file.

1.  Write a program that produces a plain-text table of contents,
    using indentation to show nesting:

    ```text
    Species Information
      Water Birds
      Loons
      Details
    ```

## Scraping the Web

The Hypertext Transfer Protocol (HTTP) specifies one way that
programs can exchange data over the Internet.
HTTP is deliberately simple:
the client sends a request specifying what it wants
and the server sends some data in response.
This can be the contents of a file copied from disk,
some HTML generated dynamically,
a blob of JSON (as text),
or anything else.

An HTTP request is that it's just text:
any program that wants to can create one or parse one.
An absolutely minimal HTTP request has just a *method* (sometimes also called a *verb*),
a *URL*,
and a *protocol version*
on a single line separated by spaces like this:

```
GET /index.html HTTP/1.1
```

The HTTP method is almost always either `GET` (to fetch information)
or `POST` (to submit form data or upload files).
The URL specifies what the client wants;
it is often a path to a file on disk,
such as `/index.html`,
but again,
the server can interpret it however it wants.
The HTTP version is usually "HTTP/1.0" or "HTTP/1.1";
the differences between the two don't matter to us.

Most real requests have a few extra lines called *headers*,
which are key value pairs like the three shown below:

```
GET /index.html HTTP/1.1
Accept: text/html
Accept-Language: en, fr
If-Modified-Since: 16-May-2022
```

Unlike the keys in hash tables,
keys may appear any number of times in HTTP headers.
This allows a request to do things like
specify that it's willing to accept several types of content.

Finally,
the *body* of the request is any extra data associated with the request;
if there is a body,
the request must have a header called `Content-Length`
that tells the server how many bytes to read in the body of the request.
The body is used for submitting data via web forms,
uploading files,
and so on.
There must be a blank line between the last header and the start of the body
to signal the end of the headers.

An HTTP response is formatted like an HTTP request.
Its first line has the protocol,
a *status code* like 200 or 404,
and a status phrase like "OK" or "Not Found".
There are then some headers,
a blank line,
and the body of the response:

```
HTTP/1.1 200 OK
Date: Thu, 16 June 2022 12:28:53 GMT
Server: minserve/2.2.14 (Linux)
Last-Modified: Wed, 15 Jun 2022 19:15:56 GMT
Content-Type: text/html
Content-Length: 53

<html>
<body>
<h1>Hello, World!</h1>
</body>
</html>
```

Constructing HTTP requests is tedious,
so most people use libraries to do most of the work.
The most popular such library in Python is called [requests][requests].
Since `species.html` is stored in a public GitHub repository,
it can be viewed online at <https://gvwilson.github.io/tlscr/species.html>.
Here's a program that uses requests to download and print the source:

```python
import requests

URL = "https://gvwilson.github.io/tlscr/species.html"

response = requests.get(URL)
print(f"status code: {response.status_code}")
print("text:")
print(request.text)
```
```text
status code: 200
text:
<html>
  <head>
    <title>Species Information</title>
  </head>
  <body>
    <h1>Species Information</h1>
    …as previously…
  </body>
</html>
```

Once we have the HTML text,
we can parse it with Beautiful Soup.
We can then look for hypertext links
(i.e., elements with the `a` tag and an `href` attribute)
and download the pages that this one refers to.

### Exercises (for the week of July 5-12)

The page <https://gvwilson.github.io/tlscr/species-index.html>
has the following content:

```html
<html>
  <head>
    <title>Species Information</title>
  </head>
  <body>
    <h1>Species Information</h1>
    <p>
      All information from
      <a href="https://en.wikipedia.org/wiki/List_of_birds_of_Ontario">Wikipedia</a>.
    </p>
    <ul>
      <li><a href="snow-goose.html" class="species">Snow goose</a></li>
      <li><a href="nonexistent-loon.html" class="species">Nonexistent loon</a></li>
      <li><a href="mute-swan.html" class="species">Mute swan</a></li>
      <li><a href="green-winged-teal.html" class="species">Green-winged teal</a></li>
      <li><a href="smew.html" class="species">Smew</a></li>
      <li><a href="histrionic-duck.html" class="species">Histrionic duck</a></li>
    </ul>
  </body>
</html>
```

1.  Modify the Python program shown earlier to download this page,
    parse it with Beautiful Soup,
    and show a list of species' names.

2.  Modify the program you just wrote to download this page,
    find all the links with the class `"species"`,
    download *those* pages,
    and print the scientific name of each species.
    For reference,
    the sub-page for smews is shown below.

```html
<html>
  <head>
    <title>Smew</title>
  </head>
  <body>
    <h1>Smew</h1>
    <p class="scientific">Mergellus albellus</p>
  </body>
</html>
```

Note: you may find `urllib.parse` useful for constructing the URLs of pages.
In particular:

```
>>> from urllib.parse import urlparse
>>> components = urlparse("https://gvwilson.github.io/tlscr/species-index.html")
>>> components.scheme
"https"
>>> components.netloc
"gvwilson.github.io"
>>> components.path
"/tlscr/species-index.html"
```

[bs]: https://www.crummy.com/software/BeautifulSoup/
[requests]: https://docs.python-requests.org/
