
from bs4 import BeautifulSoup
import re
"""
Write a program to count the number of tables in table.html.
"""
def count_tables(filename):
  with open(filename,'r') as readfile:
    doc = BeautifulSoup(readfile, "html.parser")
    tables = len(doc.find_all("table"))
  return tables

print(count_tables("table.html"))
"""

## Comments

* img tag don't have closing tag - so use find_all (nodes)
* iterator knows how to return the next value (instead of generate the entire list)
  * saves memory - two numbers (what's the next and when to stop)
  * ex. reading lines from a file is just next - (only store that much in memory)
  * sometimes iterator hasn't been converted to list of values
  * generator = iterator on steroid (can do more)
    * gives yield instead of return

"""

"""

Write a program that combines all the information from tables with the class species into a single CSV file.

* define intermediate points - easier to debug with breakpoint
* Erratum: th for table header instead of td (line 9 and 18)
* there is even thead (headers) and tbody (table body)
  * machine generated page will do this
* tidyverse generated tables all have that

* sends request - get response
* 200 or 404 or 403 (no permission)
  * has body - what the response was
* have to stop infinite recursion (relative link & absolute link & domain name in or out)
  * hard to get canonical URL

"""
def get_classes(filepath):
  with open('table.csv','w') as writer:
    with open(filepath,'r') as readfile:
      doc = BeautifulSoup(readfile,"html.parser")
      # tables = doc.find_all("tables", attrs={"class": "species"})
      tables = doc.find_all("table", attrs={"class": "species"})
      for table in tables:
        rows = table.findChildren('tr')
        for row in rows:
          cells = row.findChildren('td')
          row_info = []
          for cell in cells:
            cell_content = cell.getText().strip()
            row_info.append(cell_content)
            # print(cell_content)
          row_info.append('\n')
          writer.write(",".join(row_info))

get_classes("table.html")

"""
Write a program that produces a plain-text table of contents, using indentation to show nesting:

```
Species Information
  Water Birds
  Loons
  Details
```

"""

def output_txt(filepath):
  with open(filepath,'r') as readfile:
    doc = BeautifulSoup(readfile,"html.parser")
    header1 = doc.find("h1")
    print(header1.getText())
    header2 = doc.find_all("h2")
    for h2 in header2:
      print('\t' + h2.getText())



output_txt("table.html")




