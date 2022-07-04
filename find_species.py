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
