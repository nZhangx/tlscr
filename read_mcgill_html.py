import codecs
from bs4 import BeautifulSoup


path = "/Users/nicolezhang/Documents/mcgill_med/Student Schedule by Course Section.html"
f = codecs.open(path, 'r', 'utf-8')
document= BeautifulSoup(f.read()).get_text()
print(document)

for line in document:
    line = line.replace('\n','')


# all lines in class dddefault