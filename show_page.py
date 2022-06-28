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
