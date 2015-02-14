"""
 This file screen scraps the yahoo website and gathers
 all stock ticker symbols for a given industry. You specify
 which industry you're interested in in the INDUSTRIES list

 The output will be a file in the data directory, 1 file
 per industry with company name along with it's ticker symbol

"""

import urllib2
from pyquery import PyQuery as pq


# This is the root page that contains the industries
BASE_URL = "http://biz.yahoo.com/p/"

# List of industry names, and urls
INDUSTRIES = [("Technology", BASE_URL + "8conameu.html"),
              ("Finance", BASE_URL + "4conameu.html")]


def get_url(url):
    return urllib2.urlopen(url).read()


def get_symbol(sub_industry, symbols):
    print sub_industry[0] + " " + BASE_URL + sub_industry[1]

    page = pq(get_url(BASE_URL + sub_industry[1]))
    sym_list = page("table table tr td:first font")[6:]

    for sym in sym_list:

        elem = pq(sym)
        value = elem.find('a').eq(0).text().replace("\n", " ")
        key = elem.find('a').eq(1).text()

        # in the odd case the symbol doesn't appear
        if len(key) == 0:
            continue

        symbols[key] = value


def process_industry(industry):
    symbols = {}
    page = pq(get_url(industry[1]))

    # get sub-industries
    sub_industry = page("table table tr td:first a")

    for link in sub_industry:
        elem = pq(link)
        sub = (elem.find("font").text().replace("\n", " "), elem.attr("href"))

        get_symbol(sub, symbols)

    return symbols


def print_to_file(symbols, industry_name):
    f = open("data/" + industry_name + '.csv', 'w')

    keys = symbols.keys()
    keys.sort()

    for key in keys:

        try:
            f.write(key + ";" + symbols[key] + "\n")
        except:
            print "unable to print --> " + key + " " + symbols[key]


for industry in INDUSTRIES:
    symbols = process_industry(industry)
    print_to_file(symbols, industry[0])

print 'done'


