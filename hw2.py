
from bs4 import BeautifulSoup

"""
Write a program to count the number of tables in table.html.
"""
def count_tables(filename):
  with open(filename,'r') as readfile:
    doc = BeautifulSoup(readfile, "html.parser")
    tables = doc.find("table")
    counts = 0
    for i,node in enumerate(tables):
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
            cell_content = cell.getText()
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





