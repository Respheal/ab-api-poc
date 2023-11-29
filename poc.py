# requests
# beautifulsoup4
# lxml
# types-requests
# types-beautifulsoup4
# types-lxml

import requests

from lxml import etree
from bs4 import BeautifulSoup
from urllib.parse import urlparse

headers = {"User-Agent": "Mozilla/5.0"}
first_url = "https://comic.galebound.com/comic/1#page"
second_url = "https://comic.galebound.com/comic/2#page"
page = requests.get(first_url, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")  # bs html parser
dom = etree.HTML(str(soup))  # For xpath searching
# https://lxml.de/xpathxslt.html

# tag finder
subpath = f"{urlparse(second_url).path}"
tagtypes = ["id", "rel", "class", "title"]
elementtypes = ["link", "a"]
# it was only luck that makes this work. Searching for 'a' first brings
# up a large list. The found identifier needs to produce only one link

# loop through elementtypes and tagtypes to find an XPath string that results
# in the target "Next Page" url. Grab an identifying attribute.
for element in elementtypes:
    for tagtype in tagtypes:
        realstring = f'//{element}[contains(@href,"{subpath}")]/@{tagtype}'
        identifier_list = dom.xpath(realstring)
        if identifier_list:
            identifier = identifier_list[0]
            tag = tagtype
            break
    if identifier:
        found_element = element
        break

print(f"Element: {found_element}; Tag: {tag}; Identifier: {identifier}")


# Grab the url for the next page using the found element/tag/identifier
finderstring = f"//{found_element}[contains(@{tag}, '{identifier}')]/@href"
next_page = urlparse(dom.xpath(finderstring)[0])
# store the finderstring in the db for each comic and then that's all that's
# needed to find the next page ever
# I'm realizing that some edge cases may need beyond even just the string
# unfortunately. For example, the bastards the result in infinite crawling.
# The stored string thing might work, but probably should still be able
# to specify completely unique crawler *functions* that can be called
# for the true edge cases. This also goes for known crawler types such as
# webtoons and tapas which would have their own specifications e.g. api read
# So maybe the DB is like, "crawler" "crawler params"?
# That's....not that different. But betterer, one hopes.

parsed_url = urlparse(first_url)  # to break the url into workable pieces
print(f"Current Page: {first_url}")
print(
    f"Next Page: {parsed_url.scheme}://{parsed_url.hostname}{next_page.path}"
)
