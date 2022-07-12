import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# added functions
def parse_sublink(sublink):
    # return specifically scientific name
    response = requests.get(sublink)
    if response.status_code != 404:
        doc = BeautifulSoup(response.text,'html.parser')
        # print(doc)
        strs = doc.find_all('p',attrs={"class":"scientific"})
        # print(strs)
        allcontents = []
        for st in strs:
            allcontents.append(st.contents[0])
        return allcontents
    else:
        print("link {} does not exist".format(sublink))
        return None

def assemble_sublink(location,newlink):
    """ assemble new link from relative links (newlink) and original full path link (location) """
    return requests.compat.urljoin(location,newlink)

def findall_list(sublink):
    txt = requests.get(sublink).text
    doc = BeautifulSoup(txt,'html.parser')
    species = doc.find_all("li")
    # cannot subset to attrs={"class": "species"} because the class is in the href
    sp_parsed = []
    for sp in species:
        wdrs = sp.getText().strip()
        sp_parsed.append(wdrs)
    return sp_parsed

def findall_link(sublink):
    baselink = urlparse(sublink)
    txt = requests.get(sublink).text
    doc = BeautifulSoup(txt,'html.parser')
    species = doc.find_all('a',href = True,attrs={"class": "species"})
    listofsp = []
    for spr in species:
        # print(spr['href'])
        link = spr['href']
        assembled_link = assemble_sublink(sublink, link)
        print(assembled_link)
        end = parse_sublink(assembled_link)
        if not end is None:
            listofsp.append(end) 
    # print(species)
    return listofsp


# input URL
URL = "https://gvwilson.github.io/tlscr/species-index.html"
components = urlparse(URL)


response = requests.get(URL)
print(f"status code: {response.status_code}")



"""
Q1
"""
print(findall_list(URL))

"""
Q2
"""
print(findall_link(URL))



