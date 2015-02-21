import re
from datetime import datetime
from pyquery import PyQuery as pq

# Take the text from markup and convert to
# float value before we persist to database
def string_to_float(value):
    try:
        toRet = float(value)
    except:
        toRet = "N/A"

    return toRet

# Dates are bit tricky because they don't
# seem to be stored in a consistent format
# also they are non-standard
def parse_date(value):

    if len(value) == 0:
        return "N/A"

    # May 12 - May 24 (Est.)
    exp = re.match(r'(\w{3}\s*\d{1,2})\s*-\s*(\w{3}\s*\d{1,2}).', value.strip(), re.I)
    if exp:
        date = exp.group(1) + " 2015"
        return datetime.strptime(date, '%b %d %Y')

    # 12-apr-15
    exp = re.match(r'(\d{1,2}-\w{3}-\d{1,2})', value.strip(), re.I)
    if exp:
        date = exp.group(1)
        return datetime.strptime(date, '%d-%b-%y')

    return "N/A"


def Symbol(content, name, ticker):
    dom = pq(content)
    col1 = dom.find("#table1 .yfnc_tabledata1")
    col2 = dom.find("#table2 .yfnc_tabledata1")

    if len(col1) == 0 or len(col2) == 0:
        return None

    obj = {}

    obj["name"] = name.strip().replace("\n", "")
    obj["_id"] = ticker

    # get header info
    obj["price"] = string_to_float(dom.find(".time_rtq_ticker span").text())

    # get first column
    obj["prev_close"] = string_to_float(pq(col1[0]).text())
    obj["open"] = string_to_float(pq(col1[1]).text())
    obj["beta"] = string_to_float(pq(col1[5]).text())
    obj["earnings_date"] = parse_date(pq(col1[6]).text())

    # get second column
    day_range = pq(col2[0]).text().split("-")
    year_range = pq(col2[1]).text().split("-")
    div_yield = pq(col2[7]).text().split(" ")

    if len(day_range) > 1:
        obj["day_low"] = string_to_float(day_range[0])
        obj["day_high"] = string_to_float(day_range[1])

    if len(year_range) > 1:
        obj["year_low"] = string_to_float(year_range[0])
        obj["year_high"] = string_to_float(year_range[1])

    obj["market_cap"] = pq(col2[4]).text()
    obj["pe"] = string_to_float(pq(col2[5]).text())
    obj["eps"] = string_to_float(pq(col2[6]).text())

    if len(div_yield) > 1:
        obj["div_yield_dollar"] = string_to_float(div_yield[0])
        obj["div_yield_percent"] = string_to_float(re.sub("[()%]", "", div_yield[1]))

    obj["daily_dollar_gain"] = obj["price"] - obj["prev_close"]
    obj["daily_percentage_gain"] = round(((obj["price"] - obj["prev_close"])/obj["prev_close"]) * 100, 2);


    return obj
