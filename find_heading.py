from bs4 import BeautifulSoup

with open("species.html", "r") as reader:
    doc = BeautifulSoup(reader, "html.parser")
    heading = doc.find("h1")
    print(heading.string)
