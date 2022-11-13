## This script generates the file index.html in the folder passed as a parameter
## Parameters : (1) deploy folder (2) language subfolder
import sys
import yaml

lang = sys.argv[2]

# Read config
with open("_config.yml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

books = config["booknames"][lang]
books_cropped = [book.replace(" ","") for book in books ]

from templateIndex import templateIndex, templateIndexLink
from templateFooter import templateFooter


prepared_index_links = [templateIndexLink.format(lang, book_cropped, book) for book, book_cropped in zip(books, books_cropped)  ]

with open(f"{sys.argv[1]}/{lang}/index.html","w+") as fout:
    fout.write(templateIndex.format(
        sitename = config["sitename"][lang],
        sitesubname = config["sitesubname"][lang],
        largedescription = config["largedescription"][lang],
        heading_part1 = config["words"]["heading_part1"][lang],
        heading_part2 = config["words"]["heading_part2"][lang],
        heading_part3 = config["words"]["heading_part3"][lang],
        links1 = "".join(prepared_index_links[:5]),
        links2 = "".join(prepared_index_links[5:21]),
        links3 = "".join(prepared_index_links[21:]),
        footer = templateFooter.format(""),
        lang = lang
        ) )