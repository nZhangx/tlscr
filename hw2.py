
from bs4 import BeautifulSoup
import re
"""
Write a program to count the number of tables in table.html.
"""
def count_tables(filename):
  with open(filename,'r') as readfile:
    doc = BeautifulSoup(readfile, "html.parser")
    tables = doc.find("table")
    counts = 0
    for i, __ in enumerate(tables):
      counts = i
      # print(i)
      # print(node)
  return counts//2

print(count_tables("table.html"))

"""

Write a program that combines all the information from tables with the class species into a single CSV file.

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




